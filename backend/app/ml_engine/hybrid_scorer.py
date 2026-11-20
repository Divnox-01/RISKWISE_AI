from typing import Dict, Any

class HybridRiskScorer:
    """
    Combines Supervised XGBoost Fraud Probability, Unsupervised Isolation Forest Anomaly Index,
    and Behavioural Rule Engine score into a unified 0-100 composite risk index.
    """
    def __init__(
        self,
        weight_xgb: float = 0.60,
        weight_iforest: float = 0.25,
        weight_rules: float = 0.15,
        threshold_medium: float = 35.0,
        threshold_high: float = 65.0
    ):
        self.w_xgb = weight_xgb
        self.w_iforest = weight_iforest
        self.w_rules = weight_rules
        self.threshold_medium = threshold_medium
        self.threshold_high = threshold_high

    def compute_risk(self, xgb_prob: float, iforest_score: float, rule_score: float) -> Dict[str, Any]:
        # Weighted linear combination scaled to 0-100
        raw_composite = (self.w_xgb * xgb_prob) + (self.w_iforest * iforest_score) + (self.w_rules * rule_score)
        risk_score = round(max(0.0, min(100.0, raw_composite * 100.0)), 2)

        if risk_score >= self.threshold_high:
            category = "High Risk"
            recommendation = "BLOCK"
            action_description = "Transaction exceeds critical fraud risk threshold (>= 65). Immediate block and priority analyst alert initiated."
        elif risk_score >= self.threshold_medium:
            category = "Medium Risk"
            recommendation = "REVIEW"
            action_description = "Elevated risk profile detected (35 - 64.9). Flagged for step-up biometric/SMS authorization or manual queue review."
        else:
            category = "Low Risk"
            recommendation = "ALLOW"
            action_description = "Transaction within normal operational tolerance (< 35). Automated clearing approved."

        return {
            "risk_score": risk_score,
            "risk_category": category,
            "recommended_action": recommendation,
            "action_description": action_description,
            "score_breakdown": {
                "xgb_fraud_probability": round(float(xgb_prob), 4),
                "xgb_weighted_contribution": round(float(self.w_xgb * xgb_prob * 100), 2),
                "isolation_forest_anomaly_score": round(float(iforest_score), 4),
                "isolation_forest_weighted_contribution": round(float(self.w_iforest * iforest_score * 100), 2),
                "rule_engine_score": round(float(rule_score), 4),
                "rule_engine_weighted_contribution": round(float(self.w_rules * rule_score * 100), 2)
            },
            "weights": {
                "xgboost": self.w_xgb,
                "isolation_forest": self.w_iforest,
                "rule_engine": self.w_rules
            },
            "disclaimer": "The composite risk score is a composite multi-signal triage index and not a single calibrated Bayesian probability."
        }
