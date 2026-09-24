# ExpenseMate - Personal Expense Manager

ExpenseMate is a layered desktop application for recording personal income and
expenses. It uses Python, Tkinter, SQLite, and Matplotlib.

## Features

- Add income and expense transactions with validation.
- View transactions and delete a selected transaction.
- Set monthly category budgets with OK, warning, and exceeded alerts.
- Select a month and year for summaries, budgets, and analytics.
- View expense totals by category in a pie chart.
- Import and export transactions as CSV files.
- Create recurring monthly transactions with end-of-month date handling.

## Architecture

The project uses a layered architecture:

- `src/ui.py`: Tkinter presentation layer.
- `src/logic.py`: validation, summaries, budgets, analytics, and CSV rules.
- `src/db.py`: SQLite data-access layer and schema management.
- `src/main.py`: application entry point.

## Setup

Use Python 3.10 or newer. From the `Expense-Mate` directory:

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

## Run

```bash
python src/main.py
```

The SQLite database is created automatically at `data/expensemate.db`.

## Test

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

The test suite covers database CRUD, validation, summaries, budget alerts,
recurring transactions, and CSV import/export.

## Sample data

`data/sample_import.csv` can be imported from the Import / Export tab.