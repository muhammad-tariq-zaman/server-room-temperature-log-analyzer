import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from main import analyze

def row(timestamp, sensor, temp):
    return {"timestamp": timestamp, "sensor": sensor, "temperature_c": str(temp)}

SAMPLE = [row("2026-11-12 08:00", "Rack-A-Intake", 24.5),
          row("2026-11-12 09:00", "Rack-A-Intake", 26.8),
          row("2026-11-12 10:00", "Rack-A-Intake", 29.4),
          row("2026-11-12 11:00", "Rack-A-Intake", 33.2),
          row("2026-11-12 12:00", "Rack-A-Intake", 27.5),
          row("2026-11-12 08:00", "Rack-B-Intake", 25.0),
          row("2026-11-12 09:00", "Rack-B-Intake", 28.1),
          row("2026-11-12 10:00", "Rack-B-Intake", 31.5),
          row("2026-11-12 11:00", "Rack-B-Intake", 32.8),
          row("2026-11-12 12:00", "Rack-B-Intake", 26.0)]

class TestTemperatureLog(unittest.TestCase):
    def test_average_and_extremes(self):
        results, _ = analyze(SAMPLE)
        rack_a = [r for r in results if r[0] == "Rack-A-Intake"][0]
        self.assertEqual((rack_a[2], rack_a[3], rack_a[4]), (28.3, 24.5, 33.2))

    def test_over_warn_count(self):
        results, _ = analyze(SAMPLE)
        rack_a = [r for r in results if r[0] == "Rack-A-Intake"][0]
        self.assertEqual(rack_a[5], 3)

    def test_critical_count(self):
        results, critical = analyze(SAMPLE)
        rack_b = [r for r in results if r[0] == "Rack-B-Intake"][0]
        self.assertEqual(rack_b[6], 1)
        self.assertEqual(len(critical), 2)

    def test_exactly_warn_is_not_over(self):
        results, _ = analyze([row("2026-11-12 08:00", "S1", 27.0)])
        self.assertEqual(results[0][5], 0)

    def test_exactly_critical_counts(self):
        results, critical = analyze([row("2026-11-12 08:00", "S1", 32.0)])
        self.assertEqual(results[0][6], 1)
        self.assertEqual(len(critical), 1)

    def test_hottest_first(self):
        results, _ = analyze(SAMPLE)
        self.assertEqual(results[0][0], "Rack-A-Intake")

    def test_custom_thresholds(self):
        results, _ = analyze(SAMPLE, warn=30.0, critical=33.0)
        rack_a = [r for r in results if r[0] == "Rack-A-Intake"][0]
        self.assertEqual((rack_a[5], rack_a[6]), (1, 1))

    def test_empty_input(self):
        self.assertEqual(analyze([]), ([], []))
