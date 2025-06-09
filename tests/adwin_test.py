# tests/test_adwin.py

from src.adwin.detector import DriftDetector


def test_adwin_detects_spike():
    # Use smaller delta for higher sensitivity
    detector = DriftDetector(delta=0.005)

    zone = "TestZone"
    baseline = [50] * 50   # shorter baseline
    spike = [200] * 15     # 4x increase, more persistent

    # Baseline phase - should not detect drift
    for value in baseline:
        drift, mean = detector.update(zone, value)
        assert drift is False

    # Spike phase - should detect drift
    detected = False
    for i, value in enumerate(spike):
        drift, mean = detector.update(zone, value)
        if drift:
            detected = True
            print(f"Drift detected at spike {i+1}: value={value}, mean={mean:.1f}")
            break

    assert detected is True, "ADWIN should detect spike"
