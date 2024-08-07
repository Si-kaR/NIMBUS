class ExpenseTracking:
    def __init__(self):
        self.expenses = {}

    def add_expense(self, username, expense):
        if username not in self.expenses:
            self.expenses[username] = []
        self.expenses[username].append(expense)
        return "Expense added"

    def categorize_expense(self, username, expense_id, category):
        if username in self.expenses and expense_id < len(self.expenses[username]):
            self.expenses[username][expense_id]['category'] = category
            return "Expense categorized"
        return "Invalid expense ID"

    def view_expense_history(self, username):
        if username in self.expenses:
            return self.expenses[username]
        return "No expenses found"
