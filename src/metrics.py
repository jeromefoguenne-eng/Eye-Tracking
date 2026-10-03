"""
Module de calcul et de modélisation des métriques oculométriques.
"""
from typing import List, Dict, Any
import numpy as np


def calculate_fixation_metrics(durations_ms: List[float]) -> Dict[str, float]:
    """Calcule les statistiques descriptives sur les durées de fixation."""
    if not durations_ms:
        return {"count": 0, "mean_ms": 0.0, "std_ms": 0.0, "median_ms": 0.0}
    
    arr = np.array(durations_ms)
    return {
        "count": int(len(arr)),
        "mean_ms": float(np.mean(arr)),
        "std_ms": float(np.std(arr)),
        "median_ms": float(np.median(arr)),
        "min_ms": float(np.min(arr)),
        "max_ms": float(np.max(arr))
    }


def calculate_blink_rate(blink_count: int, duration_seconds: float) -> float:
    """Calcule le taux de clignements par minute (Blinks Per Minute - BPM)."""
    if duration_seconds <= 0:
        return 0.0
    return float((blink_count / duration_seconds) * 60.0)
