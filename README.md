# 💰 Expense Tracker

A simple desktop expense tracker built with **Python** and **Tkinter**. Record your daily spending, filter it by category, and see totals at a glance. Everything is saved automatically to a CSV file, so your data is still there the next time you open the app.


## Features

- **Add expenses** with a date, category, amount (₹) and an optional description
- **Input validation:** rejects invalid dates, empty categories, and non-numeric or non-positive amounts
- **Expense table** showing the newest expenses first
- **Filter by category** using the drop-down above the table
- **Delete** one or many selected rows (button or `Delete` key), with a confirmation prompt
- **Total spent** shown in the header at all times
- **Spending by category** panel with totals and progress bars, sorted from highest to lowest
- **Automatic saving** to `expenses.csv` (created on first run)
- No external libraries: uses only Python's standard library

## Requirements

- Python 3.8 or newer
- Tkinter (included with the standard Python installer on Windows and macOS; on some Linux distributions install it with `sudo apt install python3-tk`)

To check that Tkinter works, run `python -m tkinter`. A small test window should open.

## Getting started

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>

# 2. Run the app
python expense_tracker_gui.py
```

On some systems the command is `python3` instead of `python`.

## How to use

1. **Add an expense:** enter the date (it defaults to today, format `YYYY-MM-DD`), choose or type a category, enter the amount, add an optional description, and click **Add expense** (or press `Enter` in the description box).
2. **Filter:** use the **Filter** drop-down above the table to show a single category.
3. **Delete:** select one or more rows, then click **Delete selected** or press `Delete`.
4. **Review spending:** check the total in the header and the category breakdown in the left panel.

Built-in categories are Food, Travel, Shopping, Bills, Entertainment and Health. You can type any new category, and it will appear in the lists from then on.

## Data storage

Expenses are stored in `expenses.csv` in the folder you run the program from. The file uses these columns:

```csv
date,category,amount,description
2026-11-02,Transport,100.00,Train ticket
2026-11-01,Food,400.00,Restaurant dinner
```

You can open this file in Excel or any text editor. If you delete it, the app creates a new empty one on the next start.

## Project structure

```
.
├── expense_tracker_gui.py   # the whole application
├── expenses.csv             # created automatically on first run
├── screenshots/
│   └── screenshot.png
└── README.md
```

## How it works

| Part | What it does |
|------|--------------|
| `create_file_if_needed`, `load_expenses`, `save_all` | Read and write the CSV file with Python's `csv` module |
| `ExpenseApp` | The Tkinter window: header, Add expense form, category summary and expenses table |
| `add_expense` | Validates the input, then appends the expense to the CSV file |
| `delete_selected` | Removes the selected rows and rewrites the CSV file |
| `refresh` | Reloads the data and updates the table, total and category summary |

## Possible improvements

- Edit existing expenses
- Monthly budgets with warnings
- Date-range filters
- Charts of spending over time
- Export reports to Excel or PDF

## Author

Anshu Sharma
