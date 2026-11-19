"""Analyse a server-room temperature log per sensor.

Usage: python3 main.py readings.csv [--warn 27] [--critical 32]
CSV columns: timestamp,sensor,temperature_c.
Per sensor: reading count, average, minimum and maximum
temperature, readings over the warning threshold (--warn,
default 27 C) and readings at or over the critical threshold
(--critical, default 32 C). Sensors are listed hottest first
(by maximum temperature); critical readings are listed by
timestamp, with the hottest sensor named in the summary.
"""
import argparse, csv, sys

def analyze(rows, warn=27.0, critical=32.0):
    grouped = {}
    for row in rows:
        sensor = row["sensor"].strip()
        grouped.setdefault(sensor, []).append(
            (row["timestamp"].strip(), float(row["temperature_c"])))
    out = []
    critical_readings = []
    for sensor, readings in grouped.items():
        temps = [temp for _, temp in readings]
        average = round(sum(temps) / len(temps), 1)
        over_warn = sum(1 for temp in temps if temp > warn)
        over_critical = sum(1 for temp in temps if temp >= critical)
        out.append((sensor, len(temps), average, min(temps), max(temps),
                    over_warn, over_critical))
        for timestamp, temp in readings:
            if temp >= critical:
                critical_readings.append((timestamp, sensor, temp))
    out.sort(key=lambda r: (-r[4], r[0]))
    critical_readings.sort()
    return out, critical_readings

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    parser.add_argument("--warn", type=float, default=27.0)
    parser.add_argument("--critical", type=float, default=32.0)
    args = parser.parse_args(argv)
    with open(args.path, newline="", encoding="utf-8") as f:
        results, critical_readings = analyze(list(csv.DictReader(f)),
                                             args.warn, args.critical)
    if not results:
        print("No readings found.")
        return 0
    for sensor, count, average, minimum, maximum, over_warn, over_critical in results:
        print(f"{sensor}: {count} reading(s), avg {average:.1f} C, "
              f"min {minimum:.1f} C, max {maximum:.1f} C, "
              f"{over_warn} over {args.warn:.1f} C, "
              f"{over_critical} at/over {args.critical:.1f} C")
    if critical_readings:
        print("Critical readings:")
        for timestamp, sensor, temp in critical_readings:
            print(f"  {timestamp} {sensor} {temp:.1f} C")
    total = sum(r[1] for r in results)
    print(f"Hottest sensor: {results[0][0]} (max {results[0][4]:.1f} C). "
          f"{len(critical_readings)} critical reading(s) out of {total}.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
