import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.metrics import (
    precision_score, recall_score, f1_score,
    roc_auc_score, average_precision_score, confusion_matrix
)
from typing import Dict, Any, Tuple
import joblib

class XGBFraudClassifier:
    """
    Supervised fraud classification model using XGBoost with class imbalance correction.
    """
    def __init__(self, random_state: int = 42):
        self.random_state = random_state
        self.model = None
        self.is_fitted = False

    def fit(self, X_train: pd.DataFrame, y_train: pd.Series, X_val: pd.DataFrame = None, y_val: pd.Series = None):
        neg_count = (y_train == 0).sum()
        pos_count = (y_train == 1).sum()
        scale_pos_weight = max(1.0, float(neg_count) / float(max(1, pos_count)))
        
        self.model = xgb.XGBClassifier(
            n_estimators=200,
            learning_rate=0.05,
            max_depth=5,
            subsample=0.8,
            colsample_bytree=0.8,
            scale_pos_weight=scale_pos_weight,
            random_state=self.random_state,
            eval_metric="aucpr",
            n_jobs=-1
        )
        
        eval_set = [(X_train, y_train)]
        if X_val is not None and y_val is not None:
            eval_set.append((X_val, y_val))
            
        self.model.fit(
            X_train, y_train,
            eval_set=eval_set,
            verbose=False
        )
        self.is_fitted = True

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        if not self.is_fitted:
            raise ValueError("Model is not fitted.")
        return self.model.predict_proba(X)[:, 1]

    def evaluate(self, X_test: pd.DataFrame, y_test: pd.Series, threshold: float = 0.5) -> Dict[str, Any]:
        probs = self.predict_proba(X_test)
        preds = (probs >= threshold).astype(int)
        
        pr_auc = float(average_precision_score(y_test, probs))
        roc_auc = float(roc_auc_score(y_test, probs))
        prec = float(precision_score(y_test, preds, zero_division=0))
        rec = float(recall_score(y_test, preds, zero_division=0))
        f1 = float(f1_score(y_test, preds, zero_division=0))
        cm = confusion_matrix(y_test, preds).tolist()
        
        return {
            "pr_auc": round(pr_auc, 4),
            "roc_auc": round(roc_auc, 4),
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "f1_score": round(f1, 4),
            "confusion_matrix": cm,
            "threshold": threshold,
            "test_sample_count": len(y_test),
            "test_fraud_count": int(y_test.sum())
        }

    def save(self, model_path: str):
        joblib.dump(self.model, model_path)

    def load(self, model_path: str):
        self.model = joblib.load(model_path)
        self.is_fitted = True
