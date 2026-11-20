import os
import json
import numpy as np
import pandas as pd
from typing import Dict, Any, Optional

from .preprocessor import PaySimPreprocessor
from .xgb_model import XGBFraudClassifier
from .isolation_forest import AnomalyDetector
from .rule_engine import BehaviouralRuleEngine
from .hybrid_scorer import HybridRiskScorer
from .shap_explainer import SHAPExplainer

class FraudInferencePipeline:
    """
    Unified production inference engine for RiskWise AI 2.0.
    Encapsulates feature preprocessing, XGBoost classification, Isolation Forest anomaly scoring,
    behavioural rule heuristics, SHAP explainability, and composite hybrid scoring.
    """
    def __init__(self, artifacts_dir: str = "backend/artifacts"):
        self.artifacts_dir = artifacts_dir
        self.preprocessor = PaySimPreprocessor()
        self.rule_engine = BehaviouralRuleEngine()
        self.hybrid_scorer = HybridRiskScorer()
        
        self.xgb_classifier = XGBFraudClassifier()
        self.anomaly_detector = AnomalyDetector()
        self.shap_explainer = None
        
        self.is_loaded = False
        self.is_demo_mode = False
        self.model_info = {}
        
        self.load_artifacts()

    def load_artifacts(self):
        xgb_path = os.path.join(self.artifacts_dir, "xgb_fraud_model.joblib")
        iso_path = os.path.join(self.artifacts_dir, "iso_forest_model.joblib")
        scaler_path = os.path.join(self.artifacts_dir, "scaler.joblib")
        schema_path = os.path.join(self.artifacts_dir, "feature_schema.json")
        bg_path = os.path.join(self.artifacts_dir, "shap_background.joblib")
        metrics_path = os.path.join(self.artifacts_dir, "metrics.json")
        
        if os.path.exists(xgb_path) and os.path.exists(iso_path) and os.path.exists(scaler_path):
            try:
                self.xgb_classifier.load(xgb_path)
                self.anomaly_detector.load(iso_path, scaler_path)
                
                if os.path.exists(bg_path):
                    self.shap_explainer = SHAPExplainer()
                    self.shap_explainer.load(self.xgb_classifier.model, bg_path)
                else:
                    self.shap_explainer = SHAPExplainer(model=self.xgb_classifier.model)
                    
                if os.path.exists(metrics_path):
                    with open(metrics_path, "r", encoding="utf-8") as f:
                        self.model_info = json.load(f)
                        
                self.is_loaded = True
                self.is_demo_mode = False
                print("ML Engine loaded successfully from serialized artifacts.")
            except Exception as e:
                print(f"Warning: Failed to load serialized artifacts ({e}). Falling back to demo mode.")
                self.is_loaded = False
                self.is_demo_mode = True
        else:
            print("Notice: Artifacts not found. Operating in synthetic demo heuristic mode.")
            self.is_loaded = False
            self.is_demo_mode = True

    def predict_transaction(self, tx_dict: Dict[str, Any]) -> Dict[str, Any]:
        # 1. Evaluate Rule Engine
        rule_eval = self.rule_engine.evaluate(tx_dict)
        rule_score = rule_eval["rule_score"]

        # 2. Extract features
        features_df = self.preprocessor.transform_single(tx_dict)

        if self.is_loaded and not self.is_demo_mode:
            # Supervised XGBoost
            xgb_prob = float(self.xgb_classifier.predict_proba(features_df)[0])
            # Unsupervised Isolation Forest
            iso_score = float(self.anomaly_detector.score(features_df)[0])
            # SHAP Explanation
            try:
                shap_explanation = self.shap_explainer.explain_instance(features_df)
            except Exception as e:
                shap_explanation = {
                    "top_risk_drivers": [],
                    "top_mitigating_factors": [],
                    "summary_insights": [f"SHAP explanation fallback: {str(e)}"],
                    "disclaimer": "SHAP calculation error fallback."
                }
        else:
            # High-fidelity demo heuristic mode (when model is not trained yet or testing demo mode)
            amount = float(tx_dict.get('amount', 0.0))
            ttype = str(tx_dict.get('type', '')).upper()
            oldbalanceOrg = float(tx_dict.get('oldbalanceOrg', 0.0))
            
            # Simulated XGBoost probability based on proven PaySim indicators
            base_prob = 0.02
            if ttype in ['TRANSFER', 'CASH_OUT']:
                base_prob += 0.20
                if amount > 150000.0:
                    base_prob += 0.40
                if oldbalanceOrg > 0 and amount >= oldbalanceOrg * 0.95:
                    base_prob += 0.30
            xgb_prob = min(0.99, max(0.01, round(base_prob + (rule_score * 0.2), 4)))
            
            # Simulated Isolation Forest anomaly score
            iso_score = min(0.95, max(0.05, round((amount / 500000.0) * 0.5 + 0.1, 4)))
            
            shap_explanation = {
                "top_risk_drivers": [
                    {"feature": "amount", "label": "Transaction Amount ($)", "shap_value": 0.35, "feature_value": amount},
                    {"feature": "orig_balance_drained", "label": "Account Balance Depletion Flag", "shap_value": 0.28, "feature_value": 1 if amount >= oldbalanceOrg else 0}
                ],
                "top_mitigating_factors": [
                    {"feature": "hour_of_day", "label": "Hour of Transaction", "shap_value": -0.05, "feature_value": tx_dict.get('step', 1) % 24}
                ],
                "summary_insights": [
                    f"Transaction amount of ${amount:,.2f} is an elevated risk driver (+0.350).",
                    "Modality flags indicate transfer/liquidation pattern."
                ],
                "disclaimer": "Demo heuristic mode explanation (models pending training)."
            }

        # 3. Compute Composite Hybrid Risk
        hybrid_res = self.hybrid_scorer.compute_risk(xgb_prob, iso_score, rule_score)

        return {
            "transaction_data": tx_dict,
            "risk_score": hybrid_res["risk_score"],
            "risk_category": hybrid_res["risk_category"],
            "recommended_action": hybrid_res["recommended_action"],
            "action_description": hybrid_res["action_description"],
            "score_breakdown": hybrid_res["score_breakdown"],
            "rules": rule_eval,
            "shap_explanation": shap_explanation,
            "engine_mode": "REAL_ML_INFERENCE" if (self.is_loaded and not self.is_demo_mode) else "DEMO_SYNTHETIC_MODE"
        }
