import os
import numpy as np
import pandas as pd
import random

def generate_synthetic_paysim(n_samples: int = 15000, seed: int = 42) -> pd.DataFrame:
    np.random.seed(seed)
    random.seed(seed)
    
    types = ['PAYMENT', 'CASH_OUT', 'CASH_IN', 'TRANSFER', 'DEBIT']
    type_probs = [0.35, 0.35, 0.20, 0.08, 0.02]
    
    steps = np.random.randint(1, 744, size=n_samples)
    steps = np.sort(steps)
    
    chosen_types = np.random.choice(types, size=n_samples, p=type_probs)
    
    amounts = []
    old_origs = []
    new_origs = []
    old_dests = []
    new_dests = []
    is_frauds = []
    is_flagged = []
    name_origs = [f"C{np.random.randint(100000000, 999999999)}" for _ in range(n_samples)]
    name_dests = [
        f"M{np.random.randint(100000000, 999999999)}" if chosen_types[i] == 'PAYMENT'
        else f"C{np.random.randint(100000000, 999999999)}"
        for i in range(n_samples)
    ]
    
    for i in range(n_samples):
        ttype = chosen_types[i]
        is_fraud = 0
        if ttype in ['TRANSFER', 'CASH_OUT']:
            if np.random.rand() < 0.035:
                is_fraud = 1
                
        if is_fraud:
            amount = round(float(np.random.exponential(scale=350000.0) + 50000.0), 2)
            amount = min(amount, 8000000.0)
            old_org = amount if np.random.rand() < 0.7 else round(amount * np.random.uniform(0.9, 1.2), 2)
            new_org = max(0.0, round(old_org - amount, 2))
            old_dst = 0.0 if np.random.rand() < 0.75 else round(float(np.random.exponential(scale=20000.0)), 2)
            new_dst = round(old_dst + amount, 2)
            flagged = 1 if amount > 200000 and ttype == 'TRANSFER' and np.random.rand() < 0.2 else 0
        else:
            if ttype == 'PAYMENT':
                amount = round(float(np.random.lognormal(mean=7.5, sigma=1.2)), 2)
                old_org = round(float(np.random.lognormal(mean=8.5, sigma=1.5)), 2)
                new_org = max(0.0, round(old_org - amount, 2))
                old_dst = 0.0
                new_dst = 0.0
            elif ttype == 'CASH_IN':
                amount = round(float(np.random.lognormal(mean=9.5, sigma=1.0)), 2)
                old_org = round(float(np.random.lognormal(mean=9.0, sigma=1.5)), 2)
                new_org = round(old_org + amount, 2)
                old_dst = round(float(np.random.lognormal(mean=9.5, sigma=1.5)), 2)
                new_dst = max(0.0, round(old_dst - amount, 2))
            elif ttype == 'CASH_OUT':
                amount = round(float(np.random.lognormal(mean=9.0, sigma=1.4)), 2)
                old_org = round(float(np.random.lognormal(mean=9.5, sigma=1.5)), 2)
                new_org = max(0.0, round(old_org - amount, 2))
                old_dst = round(float(np.random.lognormal(mean=9.0, sigma=1.5)), 2)
                new_dst = round(old_dst + amount, 2)
            elif ttype == 'TRANSFER':
                amount = round(float(np.random.lognormal(mean=10.0, sigma=1.5)), 2)
                old_org = round(float(np.random.lognormal(mean=10.5, sigma=1.5)), 2)
                new_org = max(0.0, round(old_org - amount, 2))
                old_dst = round(float(np.random.lognormal(mean=9.0, sigma=1.5)), 2)
                new_dst = round(old_dst + amount, 2)
            else:
                amount = round(float(np.random.lognormal(mean=6.5, sigma=1.0)), 2)
                old_org = round(float(np.random.lognormal(mean=8.0, sigma=1.2)), 2)
                new_org = max(0.0, round(old_org - amount, 2))
                old_dst = round(float(np.random.lognormal(mean=8.0, sigma=1.2)), 2)
                new_dst = round(old_dst + amount, 2)
            flagged = 0
            
        amounts.append(max(0.01, amount))
        old_origs.append(max(0.0, old_org))
        new_origs.append(max(0.0, new_org))
        old_dests.append(max(0.0, old_dst))
        new_dests.append(max(0.0, new_dst))
        is_frauds.append(is_fraud)
        is_flagged.append(flagged)
        
    df = pd.DataFrame({
        'step': steps,
        'type': chosen_types,
        'amount': amounts,
        'nameOrig': name_origs,
        'oldbalanceOrg': old_origs,
        'newbalanceOrig': new_origs,
        'nameDest': name_dests,
        'oldbalanceDest': old_dests,
        'newbalanceDest': new_dests,
        'isFraud': is_frauds,
        'isFlaggedFraud': is_flagged
    })
    return df

if __name__ == '__main__':
    os.makedirs('backend/data', exist_ok=True)
    df = generate_synthetic_paysim(n_samples=15000, seed=42)
    output_path = 'backend/data/paysim_synthetic.csv'
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} transactions. Frauds: {df['isFraud'].sum()} ({df['isFraud'].mean()*100:.2f}%)")
    print(f"Saved to {output_path}")
