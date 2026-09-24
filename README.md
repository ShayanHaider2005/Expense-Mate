# ExpenseMate — Personal Expense Manager

A 3-tier desktop application built with Python, Tkinter, and SQLite for tracking personal finances with budget alerting and analytics[cite: 1].

## Features
* **Transactions:** Record income/expenses with validation[cite: 1, 3].
* **Budgets:** Set monthly limits with OK/Warning/Exceeded alerts[cite: 1, 3].
* **Analytics:** Embedded Matplotlib pie charts for spending[cite: 1, 5].
* **CSV I/O:** Export data or import external files with row-skipping error reports[cite: 1, 3].
* **Recurring Transactions:** Automate fixed monthly bills (e.g., rent)[cite: 1, 3].

## Project Structure
* `src/main.py`: Entry point[cite: 1, 4].
* `src/ui.py`: Presentation layer (Tkinter GUI)[cite: 1, 5].
* `src/logic.py`: Business logic layer (Validation, Budget alerts, CSV)[cite: 1, 3].
* `src/db.py`: Data access layer (SQLite CRUD)[cite: 1, 2].
* `tests/`: Automated test suite (`test_db.py`, `test_logic.py`)[cite: 1, 6, 7].

## Quick Start
1. **Install dependency:**
   ```bash
   pip install matplotlib