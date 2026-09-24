"""Tkinter presentation layer for ExpenseMate."""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from logic import ExpenseManager, ValidationError


class ExpenseMateApp(tk.Tk):
    COLORS = {
        "navy": "#17324D", "navy_dark": "#102438", "blue": "#2F6B8A",
        "blue_light": "#DCEAF1", "background": "#F3F6F8", "surface": "#FFFFFF",
        "border": "#D8E1E7", "text": "#23313D", "muted": "#647482",
    }

    def __init__(self):
        super().__init__()
        self.title("ExpenseMate - Personal Expense Manager")
        self.geometry("980x680")
        self.minsize(820, 560)
        self.configure(background=self.COLORS["background"])
        self.manager = ExpenseManager()
        now = datetime.now()
        self.current_month = tk.IntVar(value=now.month)
        self.current_year = tk.IntVar(value=now.year)
        self._configure_styles()
        self._build_header()
        self._build_notebook()

    def _configure_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        c = self.COLORS
        style.configure("TFrame", background=c["background"])
        style.configure("Card.TFrame", background=c["surface"])
        style.configure("TLabel", background=c["background"], foreground=c["text"],
                        font=("Segoe UI", 10))
        style.configure("Muted.TLabel", background=c["surface"], foreground=c["muted"],
                        font=("Segoe UI", 9))
        style.configure("Title.TLabel", background=c["navy"], foreground="white",
                        font=("Segoe UI Semibold", 20))
        style.configure("Subtitle.TLabel", background=c["navy"], foreground="#C9D9E4",
                        font=("Segoe UI", 10))
        style.configure("Section.TLabel", background=c["background"], foreground=c["navy"],
                        font=("Segoe UI Semibold", 13))
        style.configure("TButton", padding=(14, 8), font=("Segoe UI Semibold", 10),
                        foreground=c["text"])
        style.map("TButton", background=[("active", c["blue_light"])])
        style.configure("Primary.TButton", background=c["blue"], foreground="white",
                        borderwidth=0, padding=(16, 9))
        style.map("Primary.TButton", background=[("active", c["navy"]), ("pressed", c["navy_dark"])])
        style.configure("TEntry", padding=8, fieldbackground="white", bordercolor=c["border"])
        style.configure("TNotebook", background=c["background"], borderwidth=0)
        style.configure("TNotebook.Tab", background="#E6EDF1", foreground=c["muted"],
                        padding=(16, 10), font=("Segoe UI Semibold", 10))
        style.map("TNotebook.Tab", background=[("selected", c["surface"])],
                  foreground=[("selected", c["navy"])])
        style.configure("TLabelframe", background=c["surface"], foreground=c["navy"],
                        bordercolor=c["border"], relief="solid", borderwidth=1)
        style.configure("TLabelframe.Label", background=c["surface"], foreground=c["navy"],
                        font=("Segoe UI Semibold", 11))
        style.configure("Treeview", background=c["surface"], fieldbackground=c["surface"],
                        foreground=c["text"], rowheight=32, borderwidth=0,
                        font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background=c["navy"], foreground="white",
                        relief="flat", padding=(8, 9), font=("Segoe UI Semibold", 10))
        style.map("Treeview", background=[("selected", c["blue_light"])],
                  foreground=[("selected", c["navy_dark"])])
        style.configure("Vertical.TScrollbar", background=c["border"], troughcolor=c["background"])

    def _build_header(self):
        header = tk.Frame(self, background=self.COLORS["navy"], height=86)
        header.pack(fill="x")
        header.pack_propagate(False)
        title = tk.Frame(header, background=self.COLORS["navy"])
        title.pack(fill="both", expand=True, padx=28, pady=15)
        ttk.Label(title, text="ExpenseMate", style="Title.TLabel").pack(anchor="w")
        ttk.Label(title, text="A clear view of your everyday spending",
                  style="Subtitle.TLabel").pack(anchor="w")

    def _build_notebook(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=18, pady=(10, 18))
        self.tab_add = ttk.Frame(notebook)
        self.tab_list = ttk.Frame(notebook)
        self.tab_budget = ttk.Frame(notebook)
        self.tab_analytics = ttk.Frame(notebook)
        self.tab_io = ttk.Frame(notebook)
        notebook.add(self.tab_add, text="Add Transaction")
        notebook.add(self.tab_list, text="Transactions")
        notebook.add(self.tab_budget, text="Budgets & Alerts")
        notebook.add(self.tab_analytics, text="Analytics")
        notebook.add(self.tab_io, text="Import / Export")
        self._build_add_tab()
        self._build_list_tab()
        self._build_budget_tab()
        self._build_analytics_tab()
        self._build_io_tab()

    def _card(self, parent, title):
        return ttk.LabelFrame(parent, text=title, padding=(22, 18))

    # ---------------------------------------------------------- Add tab --
    def _build_add_tab(self):
        f = self.tab_add
        f.columnconfigure(0, weight=1)
        f.rowconfigure(0, weight=1)
        card = self._card(f, "New transaction")
        card.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        card.columnconfigure(1, weight=1)
        labels = ["Type (income/expense)", "Amount", "Category", "Date (YYYY-MM-DD)", "Description"]
        self.add_vars = {k: tk.StringVar() for k in labels}
        for i, label in enumerate(labels):
            ttk.Label(card, text=label).grid(row=i, column=0, sticky="w", padx=(0, 18), pady=8)
            ttk.Entry(card, textvariable=self.add_vars[label]).grid(row=i, column=1, sticky="ew", pady=8)
        ttk.Label(card, text="Use expense or income and a positive amount.",
                  style="Muted.TLabel").grid(row=len(labels), column=1, sticky="w", pady=(2, 16))
        ttk.Button(card, text="Add Transaction", style="Primary.TButton",
                   command=self._on_add_transaction).grid(row=len(labels) + 1, column=1, sticky="w")

    def _on_add_transaction(self):
        v = self.add_vars
        try:
            self.manager.add_transaction(
                tx_type=v["Type (income/expense)"].get().strip().lower(),
                amount=float(v["Amount"].get()), category=v["Category"].get(),
                date_str=v["Date (YYYY-MM-DD)"].get().strip(), description=v["Description"].get())
            messagebox.showinfo("Success", "Transaction added.")
            for var in v.values():
                var.set("")
            self._refresh_list()
        except (ValidationError, ValueError) as e:
            messagebox.showerror("Invalid input", str(e))

    # --------------------------------------------------------- List tab --
    def _build_list_tab(self):
        f = self.tab_list
        f.columnconfigure(0, weight=1)
        f.rowconfigure(1, weight=1)
        toolbar = ttk.Frame(f)
        toolbar.grid(row=0, column=0, sticky="ew", padx=20, pady=(18, 10))
        toolbar.columnconfigure(0, weight=1)
        ttk.Label(toolbar, text="All transactions", style="Section.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Button(toolbar, text="Refresh", command=self._refresh_list).grid(row=0, column=1, sticky="e")
        table = ttk.Frame(f, style="Card.TFrame", padding=1)
        table.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        table.columnconfigure(0, weight=1)
        table.rowconfigure(0, weight=1)
        cols = ("id", "date", "type", "category", "amount", "description")
        self.tree = ttk.Treeview(table, columns=cols, show="headings")
        headings = {"id": "ID", "date": "Date", "type": "Type", "category": "Category",
                    "amount": "Amount", "description": "Description"}
        widths = {"id": 55, "date": 110, "type": 100, "category": 140, "amount": 100, "description": 260}
        for c in cols:
            self.tree.heading(c, text=headings[c])
            self.tree.column(c, width=widths[c], anchor="w")
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(table, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)
        self._refresh_list()

    def _refresh_list(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for r in self.manager.get_transactions():
            self.tree.insert("", "end", values=(r["id"], r["date"], r["type"], r["category"],
                                                 f"{r['amount']:.2f}", r["description"] or ""))

    # ------------------------------------------------------- Budget tab --
    def _build_budget_tab(self):
        f = self.tab_budget
        f.columnconfigure(0, weight=1)
        f.rowconfigure(1, weight=1)
        form = self._card(f, "Monthly budget")
        form.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 12))
        form.columnconfigure(1, weight=1)
        form.columnconfigure(3, weight=1)
        self.budget_cat = tk.StringVar()
        self.budget_limit = tk.StringVar()
        ttk.Label(form, text="Category").grid(row=0, column=0, sticky="w", padx=(0, 10))
        ttk.Entry(form, textvariable=self.budget_cat).grid(row=0, column=1, sticky="ew", padx=(0, 18))
        ttk.Label(form, text="Monthly limit").grid(row=0, column=2, sticky="w", padx=(0, 10))
        ttk.Entry(form, textvariable=self.budget_limit).grid(row=0, column=3, sticky="ew", padx=(0, 18))
        ttk.Button(form, text="Set Budget", style="Primary.TButton", command=self._on_set_budget).grid(row=0, column=4)
        alerts = self._card(f, "Budget alerts")
        alerts.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        alerts.columnconfigure(0, weight=1)
        alerts.rowconfigure(1, weight=1)
        ttk.Label(alerts, text="Current month spending against your limits",
                  style="Muted.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 10))
        self.alert_box = tk.Text(alerts, height=12, wrap="word", relief="flat", borderwidth=0,
                                 background=self.COLORS["surface"], foreground=self.COLORS["text"],
                                 font=("Segoe UI", 10), padx=8, pady=8)
        self.alert_box.grid(row=1, column=0, sticky="nsew")
        ttk.Button(alerts, text="Check Alerts (current month)", command=self._refresh_alerts).grid(
            row=2, column=0, sticky="w", pady=(12, 0))

    def _on_set_budget(self):
        try:
            self.manager.set_budget(self.budget_cat.get(), self.current_month.get(),
                                    self.current_year.get(), float(self.budget_limit.get()))
            messagebox.showinfo("Success", "Budget saved.")
            self._refresh_alerts()
        except (ValidationError, ValueError) as e:
            messagebox.showerror("Invalid input", str(e))

    def _refresh_alerts(self):
        self.alert_box.delete("1.0", tk.END)
        alerts = self.manager.check_budget_alerts(self.current_month.get(), self.current_year.get())
        if not alerts:
            self.alert_box.insert(tk.END, "No budgets set for this month yet.\n")
        for a in alerts:
            self.alert_box.insert(tk.END, f"{a['category']}: spent {a['spent']:.2f} / limit {a['limit']:.2f} "
                                         f"({a['status'].upper()})\n")

    # ---------------------------------------------------- Analytics tab --
    def _build_analytics_tab(self):
        f = self.tab_analytics
        f.columnconfigure(0, weight=1)
        f.rowconfigure(1, weight=1)
        toolbar = ttk.Frame(f)
        toolbar.grid(row=0, column=0, sticky="ew", padx=20, pady=(18, 10))
        toolbar.columnconfigure(0, weight=1)
        ttk.Label(toolbar, text="Spending by category", style="Section.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Button(toolbar, text="Refresh Chart", command=self._refresh_chart).grid(row=0, column=1, sticky="e")
        self.chart_frame = ttk.Frame(f, style="Card.TFrame")
        self.chart_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self._refresh_chart()

    def _refresh_chart(self):
        for w in self.chart_frame.winfo_children():
            w.destroy()
        data = self.manager.category_breakdown(self.current_month.get(), self.current_year.get())
        fig = Figure(figsize=(6, 4), dpi=100, facecolor=self.COLORS["surface"])
        ax = fig.add_subplot(111, facecolor=self.COLORS["surface"])
        if data:
            palette = ["#2F6B8A", "#4F8B78", "#D18B47", "#9A6A9E", "#B85C5C", "#6C8292"]
            ax.pie(data.values(), labels=data.keys(), autopct="%1.1f%%", startangle=90,
                   colors=palette[:len(data)], textprops={"color": self.COLORS["text"], "fontsize": 9},
                   wedgeprops={"linewidth": 2, "edgecolor": self.COLORS["surface"]})
            ax.set_title("Expenses by Category (this month)", color=self.COLORS["navy"],
                         fontsize=13, fontweight="bold", pad=18)
        else:
            ax.text(0.5, 0.5, "No expense data for this month", ha="center", va="center",
                    color=self.COLORS["muted"], fontsize=11)
        fig.subplots_adjust(left=0.04, right=0.96, top=0.88, bottom=0.04)
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=12, pady=12)

    # ---------------------------------------------------------- IO tab --
    def _build_io_tab(self):
        f = self.tab_io
        f.columnconfigure(0, weight=1)
        f.rowconfigure(1, weight=1)
        actions = self._card(f, "CSV data")
        actions.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 12))
        ttk.Button(actions, text="Export to CSV", command=self._on_export).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(actions, text="Import from CSV", style="Primary.TButton", command=self._on_import).grid(row=0, column=1)
        status = self._card(f, "Activity")
        status.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        status.columnconfigure(0, weight=1)
        status.rowconfigure(0, weight=1)
        self.io_status = tk.Text(status, height=10, wrap="word", relief="flat", borderwidth=0,
                                 background=self.COLORS["surface"], foreground=self.COLORS["text"],
                                 font=("Segoe UI", 10), padx=8, pady=8)
        self.io_status.grid(row=0, column=0, sticky="nsew")

    def _on_export(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv")
        if not path:
            return
        n = self.manager.export_csv(path)
        self.io_status.insert(tk.END, f"Exported {n} transactions to {path}\n")

    def _on_import(self):
        path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not path:
            return
        try:
            result = self.manager.import_csv(path)
            self.io_status.insert(tk.END, f"Imported {result['imported']}, skipped {result['skipped']}\n")
            for err in result["errors"]:
                self.io_status.insert(tk.END, f"  - {err}\n")
            self._refresh_list()
        except ValidationError as e:
            messagebox.showerror("Import failed", str(e))


if __name__ == "__main__":
    app = ExpenseMateApp()
    app.mainloop()