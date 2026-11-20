import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import RobustScaler
from typing import Tuple, Dict, Any
import joblib

class AnomalyDetector:
    """
    Unsupervised Anomaly Detector using Isolation Forest on genuine transactions.
    Scores are normalized to [0, 1] where 1 indicates extreme anomaly.
    Note: Anomaly score is an uncalibrated rarity index, not a fraud probability.
    """
    def __init__(self, contamination: float = 0.02, random_state: int = 42):
        self.contamination = contamination
        self.random_state = random_state
        self.scaler = RobustScaler()
        self.model = IsolationForest(
            n_estimators=150,
            contamination=contamination,
            random_state=random_state,
            n_jobs=-1
        )
        self.is_fitted = False

    def fit(self, X_genuine: pd.DataFrame):
        X_scaled = self.scaler.fit_transform(X_genuine)
        self.model.fit(X_scaled)
        self.is_fitted = True

    def score(self, X: pd.DataFrame) -> np.ndarray:
        if not self.is_fitted:
            raise ValueError("Model is not fitted yet.")
        X_scaled = self.scaler.transform(X)
        raw_scores = self.model.decision_function(X_scaled)
        # decision_function: lower means more anomalous (typically in range -0.5 to 0.5)
        # Normalize into [0, 1] range: 1 / (1 + exp(raw_scores * 6))
        normalized = 1.0 / (1.0 + np.exp(raw_scores * 6.0))
        return np.clip(normalized, 0.0, 1.0)

    def save(self, model_path: str, scaler_path: str):
        joblib.dump(self.model, model_path)
        joblib.dump(self.scaler, scaler_path)

    def load(self, model_path: str, scaler_path: str):
        self.model = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path)
        self.is_fitted = True
