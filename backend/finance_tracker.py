import json
import os
import bcrypt


# Define a class to represent financial transactions
class Transaction:
    def __init__(self, id, date, account, amount, notes, is_expense):
        # Initialize transaction attributes
        self.id = id
        self.date = date
        self.account = account
        self.amount = float(amount)
        self.notes = notes
        self.is_expense = is_expense

    def to_dict(self):
        # Convert transaction data to a dictionary
        return {
            "id": self.id,
            "date": self.date,
            "account": self.account,
            "amount": str(self.amount),
            "notes": self.notes,
            "is_expense": str(self.is_expense),
        }

    def __str__(self):
        # Return a string representation of the transaction
        return f"ID: {self.id}, Date: {self.date}, Account: {self.account}, Amount: {self.amount}, Notes: {self.notes}, Expense: {self.is_expense}"


# Define a class to represent user accounts and their financial data
class Account:
    def __init__(self, user_name, password_hash=None, initial_balance=0):
        # Initialize account attributes
        self.user_name = user_name
        self.password_hash = password_hash
        self.initial_balance = initial_balance
        self.transactions = []
        self.file_path = f"{user_name.lower()}_account.json"

        # Load account data if the file exists
        if os.path.exists(self.file_path):
            self.load_account_data()

    def get_initial_balance(self):
        return float(self.initial_balance)

    def calculate_balance(self):
        # Calculate the account balance based on transactions
        balance = float(self.initial_balance)

        for transaction in self.transactions:
            if transaction.to_dict()["is_expense"] == "False":
                balance += float(transaction.amount)
            else:
                balance -= float(transaction.amount)

        return balance

    def add_transaction(self, date, account, amount, notes, is_expense):
        # Add a new transaction to the account
        transaction_id = len(self.transactions) + 1
        transaction = Transaction(
            transaction_id, date, account, amount, notes, is_expense
        )
        self.transactions.append(transaction)
        self.balance = self.calculate_balance()
        self.save_account_data()

    def update_transaction(
        self, transaction_id, date, account, amount, notes, is_expense
    ):
        # Update an existing transaction in the account
        for transaction in self.transactions:
            if transaction.id == transaction_id:
                transaction.date = date
                transaction.account = account
                transaction.amount = float(amount)
                transaction.notes = notes
                transaction.is_expense = is_expense
        self.balance = self.calculate_balance()
        self.save_account_data()

    def delete_transaction(self, transaction_id):
        # Delete a transaction from the account
        for transaction in self.transactions:
            if transaction.id == transaction_id:
                self.transactions.remove(transaction)
        self.balance = self.calculate_balance()
        self.save_account_data()

    def save_account_data(self):
        # Save account data to a JSON file
        data = {
            "user_name": self.user_name,
            "password": self.password_hash.decode("utf-8")
            if self.password_hash
            else None,
            "initial_balance": self.initial_balance,
            "balance": self.calculate_balance(),
            "transactions": [
                transaction.to_dict() for transaction in self.transactions
            ],
        }

        with open(self.file_path, "w") as file:
            json.dump(data, file, indent=2)

    def load_account_data(self):
        # Load account data from a JSON file
        try:
            with open(self.file_path, "r") as file:
                data = json.load(file)

            self.user_name = data["user_name"]
            self.password_hash = (
                data["password"].encode("utf-8") if data["password"] else None
            )
            self.transactions = [
                Transaction(
                    id=transaction_data["id"],
                    date=transaction_data["date"],
                    account=transaction_data["account"],
                    amount=transaction_data["amount"],
                    notes=transaction_data["notes"],
                    is_expense=transaction_data["is_expense"],
                )
                for transaction_data in data["transactions"]
            ]

        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            print(
                f"Error loading account data for user {self.user_name}. "
                f"Please register or check if there's a typo in the username."
            )
            raise  # Optionally raise an exception to stop further execution


# Define a class to manage user registration and login
class FinanceTracker:
    def __init__(self):
        self.user_account = None

    def register(self, user_name, password, initial_balance):
        # Check if user_name or password is an empty string
        if not user_name or not password:
            print(
                "Registration unsuccessful. Please provide a valid username and password."
            )
            if not password:
                print("Please enter a password.")
            return None

        # Register a new user account
        account_file_path = f"{user_name.lower()}_account.json"

        # Check if the account file already exists
        if os.path.exists(account_file_path):
            print(
                f"Account for user {user_name} already exists. Please choose a different username."
            )
            return None

        password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        self.user_account = Account(
            user_name=user_name,
            password_hash=password_hash,
            initial_balance=initial_balance,
        )
        self.user_account.save_account_data()
        print("Backend: Registration successful.")
        return self.user_account

    def login(self, user_name, password):
        # Log in to an existing user account
        account_file_path = f"{user_name.lower()}_account.json"

        # Check if the account file exists
        if not os.path.exists(account_file_path):
            print(
                f"Account for user {user_name} does not exist. You can register to create a new account."
            )
            self.user_account = None
            return False

        # Load the data from the account file
        with open(account_file_path, "r") as f:
            data = json.load(f)

        # Extract the password hash
        password_hash = data["password"]

        # Extract the initial balance
        initial_balance = data["initial_balance"]

        self.user_account = Account(
            user_name=user_name,
            password_hash=password_hash,
            initial_balance=initial_balance,
        )

        if self.user_account.password_hash and bcrypt.checkpw(
            password.encode("utf-8"), self.user_account.password_hash
        ):
            print("Backend: Login successful.")
            return True
        else:
            print("Incorrect password. Please try again.")
            self.user_account = None
            return False
