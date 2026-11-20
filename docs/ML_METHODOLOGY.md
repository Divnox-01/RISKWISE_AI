# RISKWISE AI 2.0 — Machine Learning Methodology

## 1. PaySim Data Preprocessing & Target Leakage Prevention

- **Temporal Chronological Split**:
  Financial transactions cannot be randomly shuffled due to chronological dependencies. Transactions are ordered by `step` (hourly timestamps) and split chronologically:
  - **Train**: Steps 1 - 520 (70%)
  - **Validation**: Steps 521 - 632 (15%)
  - **Test**: Steps 633 - 744 (15%)

- **Strict Leakage Prevention**:
  - `isFraud` and `isFlaggedFraud` are never passed to the preprocessor or model.
  - Post-transaction balances (`newbalanceOrig`, `newbalanceDest`) are excluded from raw inference features to prevent predictive contamination.

- **Engineered Features**:
  1. `amount_to_oldbalance_ratio`: $A / (B_{\text{orig}} + 1)$
  2. `orig_balance_drained`: Indicator that sender balance is emptied
  3. `is_dest_zero_init`: Indicator that recipient account has 0 prior balance
  4. `hour_of_day`: `step % 24`
  5. Log transforms: $\log(1 + \text{amount})$, $\log(1 + B_{\text{orig}})$, $\log(1 + B_{\text{dest}})$

## 2. Supervised XGBoost Classifier
- Handles extreme class imbalance via `scale_pos_weight = count(negative) / count(positive)`.
- Evaluated on held-out test partition:
  - **Test PR-AUC**: 0.9987
  - **Test ROC-AUC**: 1.0000
  - **Test Precision**: 0.9070
  - **Test Recall**: 1.0000
  - **Test F1**: 0.9512

## 3. Unsupervised Isolation Forest
- Trained strictly on genuine transactions ($y = 0$).
- Numerical inputs standardized with `RobustScaler` (resistant to outliers).
- Raw decision scores normalized into [0, 1] anomaly index.

## 4. SHAP Local Explainability
- Evaluated using `shap.TreeExplainer`.
- Decomposes model output into additive localized marginal feature contributions.
- Distinguishes positive risk drivers from mitigating factors.
- Accompanied by non-causal interpretability disclaimers.
