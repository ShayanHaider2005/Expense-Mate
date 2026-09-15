# ExpenseMate — Personal Expense Manager

Software Construction Assignment 01. Client-Server (local) architecture,
Layered internally: Presentation (`ui.py`) → Business Logic (`logic.py`) →
Data Access (`db.py`), backed by SQLite.

## Requirements
- Python 3.9+
- `pip install matplotlib` (Tkinter ships with the standard CPython installer;
  on Debian/Ubuntu you may need `sudo apt install python3-tk`)

## Run the app
```bash
cd src
python main.py
```

## Run the tests
```bash
python -m unittest discover -s tests -v
```

## Project layout
```
src/
  db.py      # Data Access Layer — SQLite schema + CRUD only
  logic.py   # Business Logic Layer — validation, budgets, analytics, CSV I/O
  ui.py      # Presentation Layer — Tkinter GUI (5 tabs)
  main.py    # Entry point
tests/
  test_db.py
  test_logic.py
data/
  sample_import.csv   # Sample data for the Import/Export tab
docs/
  diagrams/            # Use case, logical/process/deployment views, Gantt chart
  *.docx               # SRS, Architecture, Test/Bug/Metrics, Maintenance, Final reports
```

## Features
- Record income/expense transactions with validation
- Monthly per-category budgets with ok / warning (≥80%) / exceeded alerts
- Category-wise analytics as a pie chart (matplotlib, embedded in the GUI)
- CSV export and CSV import (bad rows are skipped and reported, not fatal)
- Recurring monthly transactions (e.g. rent) — added in the Phase 5 maintenance cycle

## Quality
- 20 automated unit tests, 97% statement coverage on `db.py` + `logic.py`
- Average cyclomatic complexity: grade A (2.39), measured with `radon`
- Full change history in `git log` — one commit for initial construction (Phase 3),
  one for the maintenance cycle (Phase 5: 2 bug fixes + 1 new feature + refactor)
