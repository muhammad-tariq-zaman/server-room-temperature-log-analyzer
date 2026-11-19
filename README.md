# server-room-temperature-log-analyzer

Analyse a server-room temperature log per sensor: for each sensor the reading count, average, minimum and maximum temperature, readings over the warning threshold (--warn, default 27 °C) and readings at or over the critical threshold (--critical, default 32 °C) — sensors hottest first by maximum temperature, critical readings listed by timestamp, hottest sensor named in the summary.

Sample input is included (sample.csv with ten readings).

## How to run

```sh
python3 main.py sample.csv
```

## Example output

```
Rack-A-Intake: 5 reading(s), avg 28.3 C, min 24.5 C, max 33.2 C, 3 over 27.0 C, 1 at/over 32.0 C
Rack-B-Intake: 5 reading(s), avg 28.7 C, min 25.0 C, max 32.8 C, 3 over 27.0 C, 1 at/over 32.0 C
Critical readings:
  2026-11-12 11:00 Rack-A-Intake 33.2 C
  2026-11-12 11:00 Rack-B-Intake 32.8 C
Hottest sensor: Rack-A-Intake (max 33.2 C). 2 critical reading(s) out of 10.
```

Standard library only. Run the tests with `python3 -m unittest discover`.
