import numpy as np
import pandas as pd
import shap
from typing import Dict, Any, List
import joblib

FEATURE_HUMAN_NAMES = {
    'amount': 'Transaction Amount ($)',
    'oldbalanceOrg': 'Initial Sender Balance ($)',
    'oldbalanceDest': 'Initial Recipient Balance ($)',
    'amount_to_oldbalance_ratio': 'Amount-to-Balance Ratio',
    'orig_balance_drained': 'Account Balance Depletion Flag',
    'log_amount': 'Log(Amount)',
    'is_dest_zero_init': 'Zero Destination Balance Flag',
    'is_orig_zero_init': 'Zero Origin Balance Flag',
    'type_TRANSFER': 'Transfer Modality Indicator',
    'type_CASH_OUT': 'Cash-out Modality Indicator',
    'type_PAYMENT': 'Payment Modality Indicator',
    'type_CASH_IN': 'Cash-in Modality Indicator',
    'type_DEBIT': 'Debit Modality Indicator',
    'hour_of_day': 'Hour of Transaction',
    'step': 'Chronological Step'
}

class SHAPExplainer:
    """
    Explainable AI engine using SHAP TreeExplainer for tree ensemble models.
    Produces localized attribution breakdowns (positive and negative risk drivers)
    with non-causal interpretability framing.
    """
    def __init__(self, model=None, background_data: pd.DataFrame = None):
        self.model = model
        self.explainer = None
        if model is not None:
            # TreeExplainer works directly with xgboost classifier
            self.explainer = shap.TreeExplainer(model)
        self.background_data = background_data

    def fit_background(self, model, background_data: pd.DataFrame):
        self.model = model
        self.background_data = background_data
        self.explainer = shap.TreeExplainer(model)

    def explain_instance(self, X_row: pd.DataFrame, top_k: int = 5) -> Dict[str, Any]:
        if self.explainer is None:
            raise ValueError("SHAP explainer has not been initialized.")
            
        shap_values = self.explainer.shap_values(X_row)
        if isinstance(shap_values, list):
            # For binary classification some versions return [neg, pos]
            shap_vals = shap_values[1][0]
        elif len(shap_values.shape) == 2:
            shap_vals = shap_values[0]
        else:
            shap_vals = shap_values

        feature_names = X_row.columns.tolist()
        raw_values = X_row.iloc[0].to_dict()

        contributions = []
        for name, s_val in zip(feature_names, shap_vals):
            raw_val = raw_values.get(name, 0.0)
            human_label = FEATURE_HUMAN_NAMES.get(name, name)
            contributions.append({
                "feature": name,
                "label": human_label,
                "shap_value": round(float(s_val), 4),
                "feature_value": round(float(raw_val), 2) if isinstance(raw_val, (int, float, np.number)) else str(raw_val)
            })

        # Separate into risk escalators (positive SHAP) and risk mitigators (negative SHAP)
        risk_escalators = sorted(
            [c for c in contributions if c['shap_value'] > 0],
            key=lambda x: x['shap_value'],
            reverse=True
        )[:top_k]

        risk_mitigators = sorted(
            [c for c in contributions if c['shap_value'] < 0],
            key=lambda x: x['shap_value']
        )[:top_k]

        # Natural language synthesis
        insights = []
        for c in risk_escalators[:3]:
            insights.append(f"{c['label']} (value: {c['feature_value']}) elevated risk by +{c['shap_value']:.3f}.")
        for c in risk_mitigators[:2]:
            insights.append(f"{c['label']} (value: {c['feature_value']}) reduced fraud suspicion by {c['shap_value']:.3f}.")

        return {
            "top_risk_drivers": risk_escalators,
            "top_mitigating_factors": risk_mitigators,
            "all_contributions": sorted(contributions, key=lambda x: abs(x['shap_value']), reverse=True),
            "summary_insights": insights,
            "disclaimer": "SHAP feature attributions represent local additive marginal contributions to model log-odds. They do not constitute causal proof."
        }

    def save(self, bg_path: str):
        if self.background_data is not None:
            joblib.dump(self.background_data, bg_path)

    def load(self, model, bg_path: str):
        self.model = model
        self.background_data = joblib.load(bg_path)
        self.explainer = shap.TreeExplainer(model)
