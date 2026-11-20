from typing import Dict, Any, List

class BehaviouralRuleEngine:
    """
    Rule engine detecting known fraud typologies supported by PaySim patterns.
    Produces individual rule flags, severity levels, and an aggregated rule risk score (0.0 - 1.0).
    """
    def __init__(self, high_amount_threshold: float = 200000.0):
        self.high_amount_threshold = high_amount_threshold

    def evaluate(self, tx: Dict[str, Any]) -> Dict[str, Any]:
        amount = float(tx.get('amount', 0.0))
        tx_type = str(tx.get('type', '')).upper()
        oldbalanceOrg = float(tx.get('oldbalanceOrg', 0.0))
        oldbalanceDest = float(tx.get('oldbalanceDest', 0.0))
        
        triggered_rules = []
        score_accumulator = 0.0

        # Rule 1: High Transaction Amount
        if amount >= self.high_amount_threshold:
            severity = "HIGH" if amount >= 500000.0 else "MEDIUM"
            weight = 0.35 if severity == "HIGH" else 0.20
            score_accumulator += weight
            triggered_rules.append({
                "rule_id": "RULE_HIGH_AMOUNT",
                "name": "Unusually High Transaction Amount",
                "severity": severity,
                "description": f"Transaction amount of ${amount:,.2f} exceeds threshold (${self.high_amount_threshold:,.2f}).",
                "score_impact": weight
            })

        # Rule 2: Complete Origin Balance Liquidation
        if oldbalanceOrg > 0 and amount >= (oldbalanceOrg * 0.98):
            weight = 0.35
            score_accumulator += weight
            triggered_rules.append({
                "rule_id": "RULE_BALANCE_DRAIN",
                "name": "Sender Account Balance Drained",
                "severity": "HIGH",
                "description": f"Transaction of ${amount:,.2f} drains {((amount/oldbalanceOrg)*100):.1f}% of available origin balance (${oldbalanceOrg:,.2f}).",
                "score_impact": weight
            })

        # Rule 3: Zero-History Destination Account Receiving Large Funds
        if oldbalanceDest == 0.0 and amount > 50000.0:
            weight = 0.25
            score_accumulator += weight
            triggered_rules.append({
                "rule_id": "RULE_EMPTY_DEST_RECIPIENT",
                "name": "New or Zero-Balance Destination Inflow",
                "severity": "MEDIUM",
                "description": f"Large transfer (${amount:,.2f}) sent to recipient account with zero prior balance.",
                "score_impact": weight
            })

        # Rule 4: High-Risk Transaction Modality
        if tx_type in ["TRANSFER", "CASH_OUT"]:
            if tx_type == "TRANSFER" and amount > 100000.0:
                weight = 0.20
                score_accumulator += weight
                triggered_rules.append({
                    "rule_id": "RULE_LARGE_TRANSFER",
                    "name": "High Value Outward Wire/Transfer",
                    "severity": "MEDIUM",
                    "description": "High-value peer-to-peer or external bank transfer typology commonly used in fraud staging.",
                    "score_impact": weight
                })
        elif tx_type in ["PAYMENT", "DEBIT"]:
            # Typically low fraud incidence in PaySim
            pass

        # Rule 5: Zero Sender Balance Initial (Overdraft/Ghost Account)
        if oldbalanceOrg == 0.0 and amount > 1000.0 and tx_type != "CASH_IN":
            weight = 0.30
            score_accumulator += weight
            triggered_rules.append({
                "rule_id": "RULE_ZERO_BALANCE_SPEND",
                "name": "Zero Origin Balance Transaction",
                "severity": "HIGH",
                "description": f"Attempted transaction of ${amount:,.2f} from account with recorded initial balance of $0.00.",
                "score_impact": weight
            })

        normalized_rule_score = min(1.0, round(score_accumulator, 4))

        return {
            "rule_score": normalized_rule_score,
            "rules_triggered_count": len(triggered_rules),
            "flags": triggered_rules,
            "has_high_severity": any(r['severity'] == 'HIGH' for r in triggered_rules)
        }
