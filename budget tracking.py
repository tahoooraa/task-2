import json
from datetime import datetime

class Transaction:
    def __init__(self, type, category, amount, date=None):
        self.type = type  # "income" or "expense"
        self.category = category
        self.amount = amount
        self.date = date or datetime.now().strftime('%Y-%m-%d')

    def __str__(self):
        return f"{self.date} - {self.type.capitalize()}: {self.category} - ${self.amount:.2f}"

class BudgetTracker:
    def __init__(self, storage_file='transactions.json'):
        self.transactions = []
        self.storage_file = storage_file
        self.load_transactions()

    def add_transaction(self, type, category, amount):
        transaction = Transaction(type, category, amount)
        self.transactions.append(transaction)
        self.save_transactions()

    def calculate_budget(self):
        total_income = sum(t.amount for t in self.transactions if t.type == 'income')
        total_expense = sum(t.amount for t in self.transactions if t.type == 'expense')
        return total_income - total_expense

    def analyze_expenses(self):
        expense_categories = {}
        for t in self.transactions:
            if t.type == 'expense':
                if t.category not in expense_categories:
                    expense_categories[t.category] = 0
                expense_categories[t.category] += t.amount
        return expense_categories

    def save_transactions(self):
        with open(self.storage_file, 'w') as file:
            json.dump([t.__dict__ for t in self.transactions], file, default=str)

    def load_transactions(self):
        try:
            with open(self.storage_file, 'r') as file:
                transactions_data = json.load(file)
                for data in transactions_data:
                    transaction = Transaction(data['type'], data['category'], data['amount'], data['date'])
                    self.transactions.append(transaction)
        except FileNotFoundError:
            pass

    def list_transactions(self):
        for t in self.transactions:
            print(t)

def main():
    tracker = BudgetTracker()

    while True:
        print("\nBudget Tracker")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. Calculate Budget")
        print("4. Analyze Expenses")
        print("5. List Transactions")
        print("6. Exit")
        
        choice = input("Choose an option: ")

        if choice == "1":
            category = input("Enter income category: ")
            amount = float(input("Enter amount: "))
            tracker.add_transaction('income', category, amount)
        elif choice == "2":
            category = input("Enter expense category: ")
            amount = float(input("Enter amount: "))
            tracker.add_transaction('expense', category, amount)
        elif choice == "3":
            budget = tracker.calculate_budget()
            print(f"Remaining Budget: ${budget:.2f}")
        elif choice == "4":
            expenses = tracker.analyze_expenses()
            print("Expense Analysis:")
            for category, amount in expenses.items():
                print(f"{category}: ${amount:.2f}")
        elif choice == "5":
            tracker.list_transactions()
        elif choice == "6":
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
