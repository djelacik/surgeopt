# tests/test_adwin.py

from src.adwin.detector import DriftDetector


def test_adwin_detects_spike():
    detector = DriftDetector(delta=0.002)

    zone = "TestZone"
    baseline = [50] * 100  # vakaa kysyntä
    spike = [120] * 5      # äkillinen nousu

    # Ei pitäisi havaita muutosta baseline-vaiheessa
    for value in baseline:
        drift, mean = detector.update(zone, value)
        assert drift is False

    # Piikin jälkeen pitäisi havaita muutos
    detected = False
    for value in spike:
        drift, mean = detector.update(zone, value)
        if drift:
            detected = True
            break

    assert detected is True, "ADWIN should detect spike"
