import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from backend.finance_tracker import FinanceTracker

APP = FinanceTracker()


def login(username_entry, password_entry, root):
    username = username_entry.get()
    password = password_entry.get()

    if APP.login(username, password):
        root.destroy()
        Transaction()
    else:
        messagebox.showerror(
            "Login Error", "Invalid username or password. Please try again."
        )


def register(username_entry, password_entry, balance_entry, root):
    username = username_entry.get()
    password = password_entry.get()
    balance = balance_entry.get()

    if APP.register(username, password, balance):
        root.destroy()
        Transaction()
    else:
        messagebox.showerror(
            "Register Error", "Invalid username or password. Please try again."
        )


def Authentication():
    root = tk.Tk()
    root.title("Enhanced Finance Tracker")

    style = ttk.Style(root)
    root.tk.call("source", "interface/ui-theme/forest-light.tcl")
    style.theme_use("forest-light")

    frame = ttk.Frame(root)
    frame.pack()

    # Title Bar
    title_bar = ttk.Label(
        frame, text="Enhanced Finance Tracker", font=("Arial", 16, "bold")
    )
    title_bar.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    # Validation function to check if a character is numeric
    def is_numeric_input(char):
        return char.isdigit()

    # Login Form
    widgets_frame = ttk.Frame(frame)
    widgets_frame.grid(row=1, column=0, padx=40, pady=20)

    login_title_label = ttk.Label(
        widgets_frame, text="Login", font=("Arial", 12, "bold")
    )
    login_title_label.grid(row=0, column=0, pady=10)

    login_username_label = ttk.Label(widgets_frame, text="Username")
    login_username_label.grid(row=1, column=0, padx=20, sticky="w")

    login_username_entry = ttk.Entry(widgets_frame, width=40)
    login_username_entry.grid(row=2, column=0, padx=20, pady=5)

    login_password_label = ttk.Label(widgets_frame, text="Password")
    login_password_label.grid(row=3, column=0, padx=20, sticky="w")

    login_password_entry = ttk.Entry(widgets_frame, width=40, show="*")
    login_password_entry.grid(row=4, column=0, padx=20, pady=5)

    login_button = ttk.Button(
        widgets_frame,
        text="Login",
        width=39,
        style="Accent.TButton",
        command=lambda: login(login_username_entry, login_password_entry, root),
    )
    login_button.grid(row=5, column=0, padx=20, pady=5)

    # Register Form
    widgets_frame = ttk.Frame(frame)
    widgets_frame.grid(row=1, column=1, padx=40, pady=20)

    register_title_label = ttk.Label(
        widgets_frame, text="Register", font=("Arial", 12, "bold")
    )
    register_title_label.grid(row=0, column=1, pady=10)

    register_username_label = ttk.Label(widgets_frame, text="Username")
    register_username_label.grid(row=1, column=1, padx=20, sticky="w")

    register_username_entry = ttk.Entry(widgets_frame, width=40)
    register_username_entry.grid(row=2, column=1, padx=20, pady=5)

    register_password_label = ttk.Label(widgets_frame, text="Password")
    register_password_label.grid(row=3, column=1, padx=20, sticky="w")

    register_password_entry = ttk.Entry(widgets_frame, width=40, show="*")
    register_password_entry.grid(row=4, column=1, padx=20, pady=5)

    register_initial_balance_label = ttk.Label(widgets_frame, text="Initial Balance")
    register_initial_balance_label.grid(row=5, column=1, padx=20, sticky="w")

    validate_numeric_input_cmd = (widgets_frame.register(is_numeric_input), "%S")
    register_initial_balance_entry = ttk.Entry(
        widgets_frame,
        width=40,
        validate="key",
        validatecommand=validate_numeric_input_cmd,
    )
    register_initial_balance_entry.grid(row=6, column=1, padx=20, pady=5)

    register_button = ttk.Button(
        widgets_frame,
        text="Register",
        width=39,
        style="Accent.TButton",
        command=lambda: register(
            register_username_entry,
            register_password_entry,
            register_initial_balance_entry,
            root,
        ),
    )
    register_button.grid(row=7, column=1, padx=20, pady=5)

    root.mainloop()


def Transaction():
    root = tk.Tk()
    root.title("Enhanced Finance Tracker")

    style = ttk.Style(root)
    root.tk.call("source", "interface/ui-theme/forest-light.tcl")

    style.theme_use("forest-light")

    frame = ttk.Frame(root)
    frame.pack()

    # Title Bar
    title_bar = ttk.Label(
        frame, text="Enhanced Finance Tracker", font=("Arial", 16, "bold")
    )
    title_bar.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    # Panel Title
    summary_title = ttk.Label(frame, text="Summary", font=("Arial", 13, "bold"))
    summary_title.grid(row=1, column=0)

    overview_title = ttk.Label(
        frame, text="Overview", width=40, anchor="center", font=("Arial", 13, "bold")
    )
    overview_title.grid(row=1, column=1)

    # Main Panel
    # ==================================
    # Tree Panel
    treeFrame = ttk.Frame(frame)
    treeFrame.grid(row=2, column=0, pady=10, padx=10)
    treeScroll = ttk.Scrollbar(treeFrame)
    treeScroll.pack(side="right", fill="y")

    columns = ["ID", "Date", "Account", "Amount", "Notes"]
    treeview = ttk.Treeview(
        treeFrame, columns=columns, show="headings", yscrollcommand=treeScroll.set
    )

    # Set column headings
    for col in columns:
        treeview.heading(col, text=col)

    treeview.column("ID", width=20, anchor=tk.CENTER)
    treeview.column("Date", width=80, anchor=tk.CENTER)
    treeview.column("Account", width=170, anchor=tk.CENTER)
    treeview.column("Amount", width=80, anchor=tk.CENTER)
    treeview.column("Notes", width=200, anchor=tk.CENTER)

    # Populate treeview with data
    for transaction in APP.user_account.transactions:
        treeview.insert("", "end", values=list(transaction.to_dict().values()))

    treeview.pack()

    # Function to update labels when a row is selected in the treeview
    def on_treeview_select(event):
        # Get selected item's data
        selected_item = treeview.item(treeview.selection())
        selected_data = selected_item["values"]

        # Update labels in the viewing section
        if selected_data:
            id_label_var.config(text=selected_data[0])
            date_label_var.config(text=selected_data[1])
            account_label_var.config(text=selected_data[2])
            amount_label_var.config(text=selected_data[3])
            notes_label_var.config(text=selected_data[4])
        else:
            print("Selected not found")

    # Bind the function to the treeview's "<<TreeviewSelect>>" event
    treeview.bind("<<TreeviewSelect>>", on_treeview_select)

    # ==================================
    # Overview Panel
    overview_frame = ttk.Frame(frame)
    overview_frame.grid(row=2, column=1, pady=10, padx=10)

    label_font_config = ("Arial", 12)

    id_label = ttk.Label(overview_frame, text="ID: ", font=label_font_config, width=10)
    id_label.grid(row=0, column=0, sticky="w")
    id_label_var = ttk.Label(
        overview_frame, text="None", font=label_font_config, width=20
    )
    id_label_var.grid(row=0, column=1, sticky="w")

    date_label = ttk.Label(overview_frame, text="Date: ", font=label_font_config)
    date_label.grid(row=1, column=0, sticky="w")
    date_label_var = ttk.Label(overview_frame, text="None", font=label_font_config)
    date_label_var.grid(row=1, column=1, sticky="w")

    account_label = ttk.Label(overview_frame, text="Account: ", font=label_font_config)
    account_label.grid(row=2, column=0, sticky="w")
    account_label_var = ttk.Label(overview_frame, text="None", font=label_font_config)
    account_label_var.grid(row=2, column=1, sticky="w")

    amount_label = ttk.Label(overview_frame, text="Amount: ", font=label_font_config)
    amount_label.grid(row=3, column=0, sticky="w")
    amount_label_var = ttk.Label(overview_frame, text="None", font=label_font_config)
    amount_label_var.grid(row=3, column=1, sticky="w")

    notes_label = ttk.Label(overview_frame, text="Notes: ", font=label_font_config)
    notes_label.grid(row=4, column=0, sticky="w")
    notes_label_var = ttk.Label(overview_frame, text="None", font=label_font_config)
    notes_label_var.grid(row=4, column=1, sticky="w")

    button_overview_frame = ttk.Frame(overview_frame)
    button_overview_frame.grid(row=5, column=0, columnspan=2, pady=10)

    def edit_page(init_data):
        root = tk.Tk()
        root.title("Edit")

        style = ttk.Style(root)
        root.tk.call("source", "interface/ui-theme/forest-light.tcl")

        style.theme_use("forest-light")

        frame = ttk.Frame(root)
        frame.pack()

        print(init_data)
        data = []

        for transaction in APP.user_account.transactions:
            if (
                transaction.to_dict()["id"] == init_data[0]
                and transaction.to_dict()["date"] == init_data[1]
            ):
                key = list(transaction.to_dict().keys())
                data = list(map(transaction.to_dict().get, key))

        print(data)

        overview_frame = ttk.Frame(frame)
        overview_frame.grid(row=2, column=1, pady=10, padx=10)

        label_font_config = ("Arial", 12)

        id_label = ttk.Label(
            overview_frame, text="ID: ", font=label_font_config, width=10
        )
        id_label.grid(row=0, column=0, sticky="w")
        id_label_var = ttk.Label(
            overview_frame, text=data[0], font=label_font_config, width=20
        )
        id_label_var.grid(row=0, column=1, sticky="w")

        date_label = ttk.Label(overview_frame, text="Date: ", font=label_font_config)
        date_label.grid(row=1, column=0, sticky="w")
        date_label_var = ttk.Entry(overview_frame, font=label_font_config)
        date_label_var.insert(0, data[1])
        date_label_var.grid(row=1, column=1, sticky="w")

        account_label = ttk.Label(
            overview_frame, text="Account: ", font=label_font_config
        )
        account_label.grid(row=2, column=0, sticky="w")
        account_label_var = ttk.Entry(overview_frame, font=label_font_config)
        account_label_var.insert(0, data[2])
        account_label_var.grid(row=2, column=1, sticky="w")

        amount_label = ttk.Label(
            overview_frame, text="Amount: ", font=label_font_config
        )
        amount_label.grid(row=3, column=0, sticky="w")
        amount_label_var = ttk.Entry(overview_frame, font=label_font_config)
        amount_label_var.insert(0, data[3])
        amount_label_var.grid(row=3, column=1, sticky="w")

        notes_label = ttk.Label(overview_frame, text="Notes: ", font=label_font_config)
        notes_label.grid(row=4, column=0, sticky="w")
        notes_label_var = ttk.Entry(overview_frame, font=label_font_config)
        notes_label_var.insert(0, data[4])
        notes_label_var.grid(row=4, column=1, sticky="w")

        expense_label = ttk.Label(
            overview_frame, text="Expense: ", font=label_font_config
        )
        expense_label.grid(row=5, column=0, sticky="w")
        checkbutton = ttk.Combobox(overview_frame)
        checkbutton["value"] = ("True", "False")
        checkbutton.set("True" if data[5] == "True" else "False")
        checkbutton.grid(row=5, column=1, sticky="nsew")

        button_overview_frame = ttk.Frame(overview_frame)
        button_overview_frame.grid(row=6, column=0, columnspan=2, pady=10)

        def done_clicked():
            get_id = data[0]
            get_date = date_label_var.get()
            get_account = account_label_var.get()
            get_amount = amount_label_var.get()
            get_notes = notes_label_var.get()
            get_expense = checkbutton.get()

            # print(get_id, get_date, get_account, get_amount, get_notes, get_expense)
            APP.user_account.update_transaction(
                get_id, get_date, get_account, get_amount, get_notes, get_expense
            )

            # Get selected item's data
            selected_item = treeview.focus()
            treeview.item(
                selected_item,
                text="",
                values=(
                    get_id,
                    get_date,
                    get_account,
                    get_amount,
                    get_notes,
                    get_expense,
                ),
            )

            root.destroy()

        done_button = ttk.Button(
            button_overview_frame,
            text="Done",
            width=10,
            style="Accent.TButton",
            command=done_clicked,
        )
        done_button.grid(row=0, column=0, pady=5, padx=5)

        root.mainloop()

    def edit_clicked():
        # Get selected item's data
        selected_item = treeview.item(treeview.selection())
        selected_data = selected_item["values"]

        if selected_data:
            edit_page(selected_data)
        else:
            print("No Selected")

    def delete_clicked():
        # Get selected item's data
        focused_item = treeview.focus()
        selected_item = treeview.item(treeview.selection())
        selected_data = selected_item["values"]

        if selected_data:
            APP.user_account.delete_transaction(selected_data[0])
            treeview.delete(focused_item)
        else:
            print("No Selected")

    edit_button = ttk.Button(
        button_overview_frame,
        text="Edit",
        width=10,
        style="Accent.TButton",
        command=edit_clicked,
    )
    edit_button.grid(row=0, column=0, pady=5, padx=5)

    delete_button = ttk.Button(
        button_overview_frame,
        text="Delete",
        width=10,
        style="Accent.TButton",
        command=delete_clicked,
    )
    delete_button.grid(row=0, column=1, pady=5, padx=5)

    def add_page():
        root = tk.Tk()
        root.title("Add Transaction")

        style = ttk.Style(root)
        root.tk.call("source", "interface/ui-theme/forest-light.tcl")

        style.theme_use("forest-light")

        frame = ttk.Frame(root)
        frame.pack()

        overview_frame = ttk.Frame(frame)
        overview_frame.grid(row=2, column=1, pady=10, padx=10)

        label_font_config = ("Arial", 12)

        date_label = ttk.Label(overview_frame, text="Date: ", font=label_font_config)
        date_label.grid(row=1, column=0, sticky="w")
        date_label_var = ttk.Entry(overview_frame, font=label_font_config)
        date_label_var.grid(row=1, column=1, sticky="w")

        account_label = ttk.Label(
            overview_frame, text="Account: ", font=label_font_config
        )
        account_label.grid(row=2, column=0, sticky="w")
        account_label_var = ttk.Entry(overview_frame, font=label_font_config)
        account_label_var.grid(row=2, column=1, sticky="w")

        amount_label = ttk.Label(
            overview_frame, text="Amount: ", font=label_font_config
        )
        amount_label.grid(row=3, column=0, sticky="w")
        amount_label_var = ttk.Entry(overview_frame, font=label_font_config)
        amount_label_var.grid(row=3, column=1, sticky="w")

        notes_label = ttk.Label(overview_frame, text="Notes: ", font=label_font_config)
        notes_label.grid(row=4, column=0, sticky="w")
        notes_label_var = ttk.Entry(overview_frame, font=label_font_config)
        notes_label_var.grid(row=4, column=1, sticky="w")

        expense_label = ttk.Label(
            overview_frame, text="Expense: ", font=label_font_config
        )
        expense_label.grid(row=5, column=0, sticky="w")
        checkbutton = ttk.Combobox(overview_frame)
        checkbutton["value"] = ("True", "False")
        checkbutton.grid(row=5, column=1, sticky="nsew")

        button_overview_frame = ttk.Frame(overview_frame)
        button_overview_frame.grid(row=6, column=0, columnspan=2, pady=10)

        def done_clicked():
            get_date = date_label_var.get()
            get_account = account_label_var.get()
            get_amount = amount_label_var.get()
            get_notes = notes_label_var.get()
            get_expense = checkbutton.get()

            print(get_date, get_account, get_amount, get_notes, get_expense)
            APP.user_account.add_transaction(
                get_date, get_account, get_amount, get_notes, get_expense
            )

            for transaction in APP.user_account.transactions:
                if (
                    transaction.to_dict()["account"] == get_account
                    and transaction.to_dict()["notes"] == get_notes
                ):
                    treeview.insert(
                        parent="",
                        index="end",
                        values=(
                            transaction.to_dict()["id"],
                            transaction.to_dict()["date"],
                            transaction.to_dict()["account"],
                            transaction.to_dict()["amount"],
                            transaction.to_dict()["notes"],
                        ),
                    )

            root.destroy()

        done_button = ttk.Button(
            button_overview_frame,
            text="Done",
            width=10,
            style="Accent.TButton",
            command=done_clicked,
        )
        done_button.grid(row=0, column=0, pady=5, padx=5)

        root.mainloop()

    def add_clicked():
        add_page()

    add_button = ttk.Button(
        button_overview_frame,
        text="Add Transaction",
        width=25,
        style="Accent.TButton",
        command=add_clicked,
    )
    add_button.grid(row=1, column=0, pady=5, columnspan=2)

    def BalanceSection():
        root = tk.Tk()
        root.title("Balance Section")

        style = ttk.Style(root)
        root.tk.call("source", "interface/ui-theme/forest-light.tcl")

        style.theme_use("forest-light")

        frame = ttk.Frame(root)
        frame.pack()

        # Balance Label
        balance_frame = ttk.Frame(frame)
        balance_frame.grid(row=3, column=0, padx=10, pady=10, columnspan=2)

        balance_label = ttk.Label(
            balance_frame, text="Current Balance: ", font=("Arial", 13, "bold")
        )
        balance_label.grid(row=0, column=0)
        balance_var = ttk.Label(
            balance_frame, text=APP.user_account.calculate_balance(), font=("Arial", 13)
        )
        balance_var.grid(row=0, column=1)

        init_balance_label = ttk.Label(
            balance_frame, text="Initial Balance: ", font=("Arial", 13, "bold")
        )
        init_balance_label.grid(row=1, column=0)
        init_balance_var = ttk.Label(
            balance_frame,
            text=APP.user_account.get_initial_balance(),
            font=("Arial", 13),
        )
        init_balance_var.grid(row=1, column=1)

    balance_button = ttk.Button(
        button_overview_frame,
        text="Check Balance",
        width=25,
        style="Accent.TButton",
        command=BalanceSection,
    )
    balance_button.grid(row=2, column=0, pady=5, columnspan=2)

    def GraphSection():
        root = tk.Tk()
        root.title("Graph Overview")

        style = ttk.Style(root)
        root.tk.call("source", "interface/ui-theme/forest-light.tcl")

        style.theme_use("forest-light")

        frame = ttk.Frame(root)
        frame.pack()

        # Graph 01 Section
        graph_frame = ttk.Frame(frame)
        graph_frame.grid(row=4, column=0, columnspan=2)

        # Prepare data for pie chart
        accounts = []
        amounts = []
        for transaction in APP.user_account.transactions:
            accounts.append(transaction.to_dict()["account"])
            amounts.append(float(transaction.to_dict()["amount"]))

        # Create two Figures for two graphs
        fig1 = Figure(figsize=(5, 3), dpi=100)
        a1 = fig1.add_subplot(111)
        a1.pie(amounts, labels=accounts, autopct="%1.1f%%")
        a1.set_title("Distribution of Accounts")

        income = []
        expense = []
        for transaction in APP.user_account.transactions:
            if transaction.to_dict()["is_expense"] == "True":
                expense.append(float(transaction.to_dict()["amount"]))
            else:
                income.append(float(transaction.to_dict()["amount"]))

        fig2 = Figure(figsize=(5, 3), dpi=100)
        a2 = fig2.add_subplot(111)
        a2.bar(["Income", "Expense"], [sum(income), sum(expense)])
        a2.set_title("Income vs Expense")

        # Create two canvases and add them to your frame in two columns
        canvas1 = FigureCanvasTkAgg(fig1, master=graph_frame)
        canvas1.draw()
        canvas1.get_tk_widget().grid(row=0, column=0, padx=5)

        canvas2 = FigureCanvasTkAgg(fig2, master=graph_frame)
        canvas2.draw()
        canvas2.get_tk_widget().grid(row=0, column=1, padx=5)

    graph_button = ttk.Button(
        button_overview_frame,
        text="Graph Overview",
        width=25,
        style="Accent.TButton",
        command=GraphSection,
    )
    graph_button.grid(row=3, column=0, pady=5, columnspan=2)

    root.mainloop()
