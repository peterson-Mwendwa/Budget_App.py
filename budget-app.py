import json
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Define the BudgetTracker class
class BudgetTracker:
    def __init__(self):
        self.income = 0
        self.expenses = []
        self.transactions = []
        self.categories = ["Food", "Entertainment", "Bills", "Other"]
        self.recurring_expenses = []
        self.load_data()  # Load saved data when starting the app

    # Load saved data from file
    def load_data(self):
        try:
            with open('budget_data.json', 'r') as f:
                data = json.load(f)
                self.income = data['income']
                self.expenses = data['expenses']
                self.transactions = data['transactions']
                self.recurring_expenses = data['recurring_expenses']
        except (FileNotFoundError, json.JSONDecodeError):
            print("No previous data found. Starting with a clean slate.")
            self.income = 0
            self.expenses = []
            self.transactions = []
            self.recurring_expenses = []

    # Save data to a file
    def save_data(self):
        data = {
            'income': self.income,
            'expenses': self.expenses,
            'transactions': self.transactions,
            'recurring_expenses': self.recurring_expenses
        }
        with open('budget_data.json', 'w') as f:
            json.dump(data, f, indent=4)

    # Set the total income
    def set_income(self, amount):
        self.income = amount
        self.save_data()

    # Add an expense
    def add_expense(self, amount, category, recurring=False):
        if category not in self.categories:
            print("❌ Invalid category! Please choose from the following: ", ", ".join(self.categories))
            return
        if amount <= 0:
            print("❌ Expense amount must be greater than zero!")
            return
        expense = {'amount': amount, 'category': category, 'date': str(datetime.now())}
        self.expenses.append(expense)
        self.transactions.append(f"Expense of {amount} for {category} added.")
        
        if recurring:
            self.recurring_expenses.append({'amount': amount, 'category': category, 'date': str(datetime.now())})
        
        self.save_data()

    # Display all expenses with optional category filter
    def view_expenses(self, category_filter=None):
        if not self.expenses:
            print("❗ No expenses recorded yet.")
        else:
            print("💸 Expenses Overview:")
            for expense in self.expenses:
                if category_filter is None or expense['category'] == category_filter:
                    print(f"{expense['date']} - {expense['category']} - ${expense['amount']}")

    # Display income and remaining budget
    def display_budget_summary(self):
        remaining_budget = self.income - self.total_expenses()
        print(f"💰 Total Income: ${self.income}")
        print(f"💸 Total Expenses: ${self.total_expenses()}")
        print(f"🤑 Remaining Budget: ${remaining_budget}")
        self.check_budget_alerts()

    # Calculate the total expenses
    def total_expenses(self):
        return sum(expense['amount'] for expense in self.expenses)

    # Display a pie chart of expenses by category
    def display_expenses_chart(self):
        if not self.expenses:
            print("❗ No expenses to display in the chart.")
            return
        
        categories_total = {category: 0 for category in self.categories}
        
        for expense in self.expenses:
            categories_total[expense['category']] += expense['amount']
        
        # Data for chart
        categories = list(categories_total.keys())
        amounts = list(categories_total.values())

        # Create a pie chart
        plt.figure(figsize=(7, 7))
        plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
        plt.title("Expenses Breakdown by Category")
        plt.show()

    # Show a monthly summary report
    def show_monthly_report(self):
        current_month = datetime.now().month
        monthly_expenses = [expense for expense in self.expenses if datetime.strptime(expense['date'], '%Y-%m-%d %H:%M:%S.%f').month == current_month]
        
        if not monthly_expenses:
            print("❗ No expenses recorded for this month.")
            return

        total_expenses_this_month = sum(expense['amount'] for expense in monthly_expenses)
        print(f"🗓️ Monthly Expenses Report for {datetime.now().strftime('%B %Y')}:")
        for expense in monthly_expenses:
            print(f"{expense['date']} - {expense['category']} - ${expense['amount']}")
        print(f"💸 Total Expenses for the Month: ${total_expenses_this_month}")
        print(f"🤑 Remaining Budget for the Month: ${self.income - total_expenses_this_month}")

    # Check if expenses are over 80% of income and show an alert
    def check_budget_alerts(self):
        if self.total_expenses() >= 0.8 * self.income:
            print("⚠️ Warning! You have spent 80% or more of your budget.")

    # Automatically add recurring expenses
    def handle_recurring_expenses(self):
        current_date = datetime.now()
        for recurring in self.recurring_expenses:
            expense_date = datetime.strptime(recurring['date'], '%Y-%m-%d %H:%M:%S.%f')
            if (current_date - expense_date).days >= 30:  # If 30 days have passed
                print(f"🔄 Recurring expense for {recurring['category']} is due. Adding it again.")
                self.add_expense(recurring['amount'], recurring['category'], recurring=True)
                recurring['date'] = str(current_date)  # Update the recurring expense date
        self.save_data()

# Main program flow
def main():
    tracker = BudgetTracker()
    
    while True:
        tracker.handle_recurring_expenses()  # Check and add recurring expenses automatically
        print("\n----- Personal Budget Tracker 💰 -----")
        print("1. Set Total Income")
        print("2. Add Expense")
        print("3. View All Expenses")
        print("4. View Budget Summary")
        print("5. View Expenses Breakdown (Pie Chart)")
        print("6. Monthly Report")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ")

        if choice == '1':
            income = float(input("Enter your total income: $"))
            tracker.set_income(income)
        elif choice == '2':
            amount = float(input("Enter expense amount: $"))
            category = input("Enter expense category (Food, Entertainment, Bills, Other): ").capitalize()
            recurring = input("Is this a recurring expense? (y/n): ").lower() == 'y'
            tracker.add_expense(amount, category, recurring)
        elif choice == '3':
            category_filter = input("Enter category to filter by (Food, Entertainment, Bills, Other) or press Enter to view all: ").capitalize()
            tracker.view_expenses(category_filter if category_filter else None)
        elif choice == '4':
            tracker.display_budget_summary()
        elif choice == '5':
            tracker.display_expenses_chart()
        elif choice == '6':
            tracker.show_monthly_report()
        elif choice == '7':
            print("Thank you for using the Personal Budget Tracker! 💵")
            break
        else:
            print("❌ Invalid choice! Please select a valid option (1-7).")

if __name__ == "__main__":
    main()
