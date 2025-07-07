
# prufia_consciousness_observer_23_24_30.py

# Plug-and-Play Observer: Layers 23, 24, and 30 Only
# Observation-only mode: NOT tied into PRUFIA scoring engine
# Outputs values for review only – no impact on match/mismatch logic

import numpy as np
from scipy import stats
from typing import List, Dict


class LayerResult:
    def __init__(self, name: str, score: float, meta: Dict, details: Dict):
        self.name = name
        self.score = score
        self.meta = meta
        self.details = details

    def to_dict(self):
        return {
            "name": self.name,
            "score": self.score,
            "meta": self.meta,
            "details": self.details
        }


class ConsciousnessObserver:
    def __init__(self, analyzer):
        self.analyzer = analyzer  # external complexity/similarity handler

    def observe_layers(self, text: str, sentences: List[str]) -> List[LayerResult]:
        results = []

        # Layer 23: Attention Drift Signatures
        attention_drift = self._layer_23_attention_drift(sentences)
        results.append(LayerResult(
            "attention_drift_signatures", attention_drift,
            {"method": "focus_vector_analysis", "type": "mathematical"},
            {"drift": attention_drift, "natural_patterns": attention_drift > 0.5}
        ))

        # Layer 24: Stress Response Linguistics
        stress_response = self._layer_24_stress_response(sentences)
        results.append(LayerResult(
            "stress_response_linguistics", stress_response,
            {"method": "complexity_degradation_analysis", "type": "mathematical"},
            {"stress": stress_response, "natural_response": stress_response > 0.4}
        ))

        # Layer 30: Consciousness Integration Signature
        consciousness = self._layer_30_consciousness_integration(results)
        results.append(LayerResult(
            "consciousness_integration_signature", consciousness,
            {"method": "integration_analysis", "type": "mathematical"},
            {"integration": consciousness, "authentic_consciousness": consciousness > 0.8}
        ))

        return results

    def _layer_23_attention_drift(self, sentences: List[str]) -> float:
        if len(sentences) < 4:
            return 0.0
        vectors = self.analyzer.text_to_vectors(sentences)
        shifts = [np.linalg.norm(vectors[i] - vectors[i + 1]) for i in range(len(vectors) - 1)]
        return min(1.0, np.var(shifts) * 10.0)

    def _layer_24_stress_response(self, sentences: List[str]) -> float:
        if len(sentences) < 5:
            return 0.0
        complexities = [self.analyzer.calculate_complexity(s) for s in sentences]
        x = np.arange(len(complexities))
        slope, _, _, _, _ = stats.linregress(x, complexities)
        return min(1.0, abs(slope) / 5.0) if slope < -0.5 else 0.0

    def _layer_30_consciousness_integration(self, layer_results: List[LayerResult]) -> float:
        if len(layer_results) < 2:
            return 0.0
        scores = [r.score for r in layer_results if r.name.startswith("attention") or r.name.startswith("stress")]
        if not scores:
            return 0.0
        mean = np.mean(scores)
        var = np.var(scores)
        return min(1.0, mean * (1 - min(0.5, var)))


# Usage:
# observer = ConsciousnessObserver(analyzer_instance)
# result = observer.observe_layers(text, sentences)
