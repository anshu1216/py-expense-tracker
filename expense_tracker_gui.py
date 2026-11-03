"""
Python Mini Project: Expense Tracker (GUI version)

Same features as the console version, now with a Tkinter interface:
- Add an expense (date, category, amount, description)
- View, filter and delete expenses in a table
- See total spending and category-wise totals with progress bars
- Everything is saved automatically in expenses.csv (same file as the CLI version)

Run: python expense_tracker_gui.py
"""

import csv
import os
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk

FILE_NAME = "expenses.csv"
FIELDS = ["date", "category", "amount", "description"]
DEFAULT_CATEGORIES = ["Food", "Travel", "Shopping", "Bills", "Entertainment", "Health"]
ALL = "All categories"

# Colours
BG = "#f4f6fb"
CARD = "#ffffff"
ACCENT = "#4f46e5"
ACCENT_DARK = "#4338ca"
TEXT = "#1f2937"
MUTED = "#6b7280"
DANGER = "#dc2626"


# ---------- Data layer ----------
def create_file_if_needed():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=FIELDS).writeheader()


def load_expenses():
    create_file_if_needed()
    with open(FILE_NAME, "r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def save_all(expenses):
    with open(FILE_NAME, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(expenses)


# ---------- UI ----------
class ExpenseApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Expense Tracker")
        self.geometry("1020x640")
        self.minsize(900, 560)
        self.configure(bg=BG)

        self.expenses = []

        self._setup_styles()
        self._build_header()

        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)

        left = tk.Frame(body, bg=BG)
        left.grid(row=0, column=0, sticky="ns", padx=(0, 16))
        self._build_form(left)
        self._build_summary(left)

        right = tk.Frame(body, bg=CARD, highlightbackground="#e5e7eb", highlightthickness=1)
        right.grid(row=0, column=1, sticky="nsew")
        self._build_table(right)

        self.refresh()

    # ----- styling -----
    def _setup_styles(self):
        s = ttk.Style(self)
        try:
            s.theme_use("clam")
        except tk.TclError:
            pass
        s.configure("Treeview", rowheight=30, font=("Segoe UI", 10),
                    background=CARD, fieldbackground=CARD, foreground=TEXT, borderwidth=0)
        s.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"),
                    background="#eef0f7", foreground=TEXT, relief="flat")
        s.map("Treeview", background=[("selected", "#e0e7ff")], foreground=[("selected", TEXT)])
        s.configure("Bar.Horizontal.TProgressbar", troughcolor="#e5e7eb",
                    background=ACCENT, thickness=8, borderwidth=0)
        s.configure("TCombobox", padding=4)

    def _card(self, parent, title):
        card = tk.Frame(parent, bg=CARD, highlightbackground="#e5e7eb", highlightthickness=1)
        card.pack(fill="x", pady=(0, 16))
        tk.Label(card, text=title, bg=CARD, fg=TEXT,
                 font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=16, pady=(14, 8))
        inner = tk.Frame(card, bg=CARD)
        inner.pack(fill="x", padx=16, pady=(0, 16))
        return inner

    # ----- header -----
    def _build_header(self):
        header = tk.Frame(self, bg=ACCENT)
        header.pack(fill="x", pady=(0, 16))
        tk.Label(header, text="💰  Expense Tracker", bg=ACCENT, fg="white",
                 font=("Segoe UI", 18, "bold")).pack(side="left", padx=20, pady=14)
        self.total_badge = tk.Label(header, text="", bg=ACCENT, fg="white",
                                    font=("Segoe UI", 13))
        self.total_badge.pack(side="right", padx=20)

    # ----- add form -----
    def _build_form(self, parent):
        f = self._card(parent, "Add expense")
        f.columnconfigure(0, weight=1)

        self.date_var = tk.StringVar(value=datetime.today().strftime("%Y-%m-%d"))
        self.cat_var = tk.StringVar()
        self.amount_var = tk.StringVar()
        self.desc_var = tk.StringVar()

        def label(text, row):
            tk.Label(f, text=text, bg=CARD, fg=MUTED, font=("Segoe UI", 9)
                     ).grid(row=row, column=0, sticky="w", pady=(8, 2))

        label("Date (YYYY-MM-DD)", 0)
        ttk.Entry(f, textvariable=self.date_var, width=30).grid(row=1, column=0, sticky="ew")

        label("Category", 2)
        self.cat_box = ttk.Combobox(f, textvariable=self.cat_var, width=28)
        self.cat_box.grid(row=3, column=0, sticky="ew")

        label("Amount (₹)", 4)
        ttk.Entry(f, textvariable=self.amount_var, width=30).grid(row=5, column=0, sticky="ew")

        label("Description (optional)", 6)
        desc = ttk.Entry(f, textvariable=self.desc_var, width=30)
        desc.grid(row=7, column=0, sticky="ew")
        desc.bind("<Return>", lambda e: self.add_expense())

        btn = tk.Button(f, text="Add expense", command=self.add_expense, bg=ACCENT, fg="white",
                        activebackground=ACCENT_DARK, activeforeground="white", relief="flat",
                        font=("Segoe UI", 10, "bold"), cursor="hand2", pady=8)
        btn.grid(row=8, column=0, sticky="ew", pady=(16, 0))

    # ----- summary -----
    def _build_summary(self, parent):
        self.summary_inner = self._card(parent, "Spending by category")

    def _render_summary(self):
        for w in self.summary_inner.winfo_children():
            w.destroy()

        totals = {}
        for e in self.expenses:
            totals[e["category"]] = totals.get(e["category"], 0.0) + float(e["amount"])
        grand = sum(totals.values())

        if not totals:
            tk.Label(self.summary_inner, text="No expenses yet.", bg=CARD, fg=MUTED,
                     font=("Segoe UI", 10)).pack(anchor="w")
            return

        for cat, amt in sorted(totals.items(), key=lambda kv: kv[1], reverse=True):
            row = tk.Frame(self.summary_inner, bg=CARD)
            row.pack(fill="x", pady=4)
            tk.Label(row, text=cat, bg=CARD, fg=TEXT, font=("Segoe UI", 10)).pack(side="left")
            tk.Label(row, text=f"₹{amt:,.2f}", bg=CARD, fg=TEXT,
                     font=("Segoe UI", 10, "bold")).pack(side="right")
            bar = ttk.Progressbar(self.summary_inner, style="Bar.Horizontal.TProgressbar",
                                  maximum=grand, value=amt)
            bar.pack(fill="x")

    # ----- table -----
    def _build_table(self, parent):
        top = tk.Frame(parent, bg=CARD)
        top.pack(fill="x", padx=16, pady=(14, 8))
        tk.Label(top, text="All expenses", bg=CARD, fg=TEXT,
                 font=("Segoe UI", 12, "bold")).pack(side="left")

        self.filter_var = tk.StringVar(value=ALL)
        self.filter_box = ttk.Combobox(top, textvariable=self.filter_var, state="readonly", width=20)
        self.filter_box.pack(side="right")
        self.filter_box.bind("<<ComboboxSelected>>", lambda e: self._render_table())
        tk.Label(top, text="Filter:", bg=CARD, fg=MUTED,
                 font=("Segoe UI", 9)).pack(side="right", padx=(0, 6))

        wrap = tk.Frame(parent, bg=CARD)
        wrap.pack(fill="both", expand=True, padx=16)

        cols = ("date", "category", "amount", "description")
        self.tree = ttk.Treeview(wrap, columns=cols, show="headings", selectmode="extended")
        for col, text, width, anchor in [
            ("date", "Date", 110, "w"),
            ("category", "Category", 130, "w"),
            ("amount", "Amount (₹)", 110, "e"),
            ("description", "Description", 260, "w"),
        ]:
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width, anchor=anchor)
        self.tree.tag_configure("odd", background="#f9fafb")

        sb = ttk.Scrollbar(wrap, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        self.tree.bind("<Delete>", lambda e: self.delete_selected())

        bottom = tk.Frame(parent, bg=CARD)
        bottom.pack(fill="x", padx=16, pady=12)
        self.shown_label = tk.Label(bottom, text="", bg=CARD, fg=MUTED, font=("Segoe UI", 10))
        self.shown_label.pack(side="left")
        tk.Button(bottom, text="Delete selected", command=self.delete_selected, bg=CARD,
                  fg=DANGER, activebackground="#fee2e2", activeforeground=DANGER,
                  relief="flat", font=("Segoe UI", 10, "bold"), cursor="hand2"
                  ).pack(side="right")

    # ----- actions -----
    def add_expense(self):
        date = self.date_var.get().strip() or datetime.today().strftime("%Y-%m-%d")
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Invalid date", "Please use the format YYYY-MM-DD.")
            return

        category = self.cat_var.get().strip()
        if not category:
            messagebox.showerror("Missing category", "Category cannot be empty.")
            return

        try:
            amount = float(self.amount_var.get().strip())
        except ValueError:
            messagebox.showerror("Invalid amount", "Please enter a valid numeric amount.")
            return
        if amount <= 0:
            messagebox.showerror("Invalid amount", "Amount must be greater than zero.")
            return

        with open(FILE_NAME, "a", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=FIELDS).writerow({
                "date": date,
                "category": category.title(),
                "amount": f"{amount:.2f}",
                "description": self.desc_var.get().strip(),
            })

        self.amount_var.set("")
        self.desc_var.set("")
        self.refresh()

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Nothing selected", "Select one or more rows to delete.")
            return
        if not messagebox.askyesno("Delete", f"Delete {len(selected)} expense(s)?"):
            return
        remove = {int(i) for i in selected}
        self.expenses = [e for i, e in enumerate(self.expenses) if i not in remove]
        save_all(self.expenses)
        self.refresh()

    # ----- refresh -----
    def refresh(self):
        self.expenses = load_expenses()

        cats = sorted({e["category"] for e in self.expenses})
        self.cat_box["values"] = sorted(set(DEFAULT_CATEGORIES) | set(cats))
        self.filter_box["values"] = [ALL] + cats
        if self.filter_var.get() not in self.filter_box["values"]:
            self.filter_var.set(ALL)

        total = sum(float(e["amount"]) for e in self.expenses)
        self.total_badge.config(text=f"Total spent: ₹{total:,.2f}")

        self._render_table()
        self._render_summary()

    def _render_table(self):
        self.tree.delete(*self.tree.get_children())
        selected_cat = self.filter_var.get()

        rows = [(i, e) for i, e in enumerate(self.expenses)
                if selected_cat == ALL or e["category"] == selected_cat]
        rows.sort(key=lambda r: r[1]["date"], reverse=True)

        shown_total = 0.0
        for n, (i, e) in enumerate(rows):
            amt = float(e["amount"])
            shown_total += amt
            self.tree.insert("", "end", iid=str(i), tags=("odd",) if n % 2 else (),
                             values=(e["date"], e["category"], f"{amt:,.2f}", e["description"]))

        self.shown_label.config(text=f"{len(rows)} expense(s) shown  •  ₹{shown_total:,.2f}")


if __name__ == "__main__":
    create_file_if_needed()
    ExpenseApp().mainloop()
