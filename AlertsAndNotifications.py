class AlertsAndNotifications:
    def __init__(self):
        self.notifications = {}

    def add_notification(self, username, notification):
        if username not in self.notifications:
            self.notifications[username] = []
        self.notifications[username].append(notification)
        return "Notification added"

    def bill_payment_reminders(self, username):
        # Placeholder for actual bill payment reminder implementation
        return "Bill payment reminders sent"

    def budget_limit_warnings(self, username, budget_limit):
        if username in self.notifications:
            expenses = sum(expense['amount'] for expense in self.notifications[username])
            if expenses > budget_limit:
                return "Budget limit warning: Exceeded"
        return "Within budget"

    def investment_opportunities(self, username):
        # Placeholder for actual investment opportunity notification
        return "Investment opportunities notified"
