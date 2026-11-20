import numpy as np
import pandas as pd
from typing import Dict, Any, List

FEATURE_COLUMNS = [
    'step',
    'amount',
    'oldbalanceOrg',
    'oldbalanceDest',
    'type_CASH_IN',
    'type_CASH_OUT',
    'type_DEBIT',
    'type_PAYMENT',
    'type_TRANSFER',
    'log_amount',
    'log_oldbalanceOrg',
    'log_oldbalanceDest',
    'amount_to_oldbalance_ratio',
    'is_orig_zero_init',
    'is_dest_zero_init',
    'orig_balance_drained',
    'is_transfer_or_cashout',
    'hour_of_day'
]

ALL_TRANSACTION_TYPES = ['CASH_IN', 'CASH_OUT', 'DEBIT', 'PAYMENT', 'TRANSFER']

class PaySimPreprocessor:
    def __init__(self):
        self.feature_columns = FEATURE_COLUMNS
        self.transaction_types = ALL_TRANSACTION_TYPES

    def engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        
        for col in ['step', 'amount', 'oldbalanceOrg', 'oldbalanceDest']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)
                
        for t in self.transaction_types:
            df[f'type_{t}'] = (df['type'] == t).astype(int)
            
        df['log_amount'] = np.log1p(np.maximum(df['amount'], 0.0))
        df['log_oldbalanceOrg'] = np.log1p(np.maximum(df['oldbalanceOrg'], 0.0))
        df['log_oldbalanceDest'] = np.log1p(np.maximum(df['oldbalanceDest'], 0.0))
        
        df['amount_to_oldbalance_ratio'] = np.where(
            df['oldbalanceOrg'] > 0,
            df['amount'] / (df['oldbalanceOrg'] + 1.0),
            0.0
        )
        df['is_orig_zero_init'] = (df['oldbalanceOrg'] <= 0).astype(int)
        df['is_dest_zero_init'] = (df['oldbalanceDest'] <= 0).astype(int)
        df['orig_balance_drained'] = ((df['oldbalanceOrg'] > 0) & (df['amount'] >= df['oldbalanceOrg'])).astype(int)
        df['is_transfer_or_cashout'] = df['type'].isin(['TRANSFER', 'CASH_OUT']).astype(int)
        df['hour_of_day'] = (df['step'] % 24).astype(int)
        
        for col in self.feature_columns:
            if col not in df.columns:
                df[col] = 0.0
                
        return df[self.feature_columns]

    def transform_single(self, tx_dict: Dict[str, Any]) -> pd.DataFrame:
        df = pd.DataFrame([tx_dict])
        return self.engineer_features(df)
