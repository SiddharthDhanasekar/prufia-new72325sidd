
# tentacation_logic.py
# PRUFIA Tentacation Layer – Multi-trait Logic Engine
# Interprets extracted traits and flags based on risk logic

def tentacation_decision(all_metrics):
    alerts = []

    # Trap A: PF < 2 and EB > 95
    if all_metrics.get('PF', 100) < 2 and all_metrics.get('EB', 0) > 95:
        alerts.append('Trap A triggered: PF<2 + EB>95')

    # Trap B: SM = 0 and MC > 90
    if all_metrics.get('SM', 1) == 0 and all_metrics.get('MC', 0) > 90:
        alerts.append('Trap B triggered: SM=0 + MC>90')

    # Trap C: Char Entropy < 40 and Syntactic Chaos > 90
    if all_metrics.get('CharTransitionEntropy', 100) < 40 and all_metrics.get('SyntacticChaos', 0) > 90:
        alerts.append('Trap C triggered: CharEntropy<40 + SyntacticChaos>90')

    # Trap D: Compression Resistance < 60 and Frequency Deviation > 85
    if all_metrics.get('CompressionResistance', 100) < 60 and all_metrics.get('FrequencyDeviation', 0) > 85:
        alerts.append('Trap D triggered: CompressionRes<60 + FrequencyDev>85')

    # Trap E: Behavioral PGFI Display > 90 and Temporal Tempo < 15
    if all_metrics.get('PGFIDisplay', 0) > 90 and all_metrics.get('TemporalTempo', 100) < 15:
        alerts.append('Trap E triggered: PGFI Display + TemporalCollapse')

    return {
        'trap_alerts': alerts,
        'trap_count': len(alerts),
        'status': 'BLOCKED' if alerts else 'CLEAR'
    }

if __name__ == "__main__":
    sample_metrics = {
        'PF': 1.7, 'EB': 98.2,
        'SM': 0, 'MC': 95.3,
        'CharTransitionEntropy': 38.1, 'SyntacticChaos': 92.4,
        'CompressionResistance': 55.0, 'FrequencyDeviation': 87.6,
        'PGFIDisplay': 91.2, 'TemporalTempo': 12.4
    }
    result = tentacation_decision(sample_metrics)
    print(result)
