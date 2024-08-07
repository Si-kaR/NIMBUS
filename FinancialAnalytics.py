class FinancialAnalytics:
    def __init__(self, expense_tracking):
        self.expense_tracking = expense_tracking

    def spending_patterns(self, username):
        if username in self.expense_tracking.expenses:
            expenses = self.expense_tracking.expenses[username]
            categories = {}
            for expense in expenses:
                category = expense.get('category', 'Uncategorized')
                amount = expense.get('amount', 0)
                categories[category] = categories.get(category, 0) + amount
            return categories
        return "No expenses found"

    def savings_progress(self, username, income, expenses):
        if username in self.expense_tracking.expenses:
            total_expenses = sum(expense['amount'] for expense in self.expense_tracking.expenses[username])
            savings = income - total_expenses
            return savings
        return "No expenses found"

    def investment_performance(self, username, investments):
        # Placeholder for actual investment performance calculation
        return "Investment performance calculated"

