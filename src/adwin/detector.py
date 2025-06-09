# src/adwin/detector.py

from river.drift import ADWIN
from typing import Dict, Tuple


class DriftDetector:
    """
    Zone-specific ADWIN-based spike detector.
    Tracks streaming values (e.g. orders per minute) per zone.
    """
    def __init__(self, delta: float = 0.002):
        """
        Args:
            delta (float): Sensitivity parameter (lower = less sensitive).
        """
        self.detectors: Dict[str, ADWIN] = {}
        self.delta = delta

    def update(self, zone: str, value: float) -> Tuple[bool, float]:
        """
        Feed new value into ADWIN detector for the given zone.

        Args:
            zone (str): Geographic zone ID (e.g. 'Kallio').
            value (float): Aggregated value (e.g. orders per minute).

        Returns:
            Tuple[bool, float]: (is_drift, current_mean)
        """
        if zone not in self.detectors:
            self.detectors[zone] = ADWIN(delta=self.delta)

        detector = self.detectors[zone]
        detector.update(value)
        return detector.drift_detected, detector.estimation
