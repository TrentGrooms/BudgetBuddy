from abc import ABC, abstractmethod
class Entry(ABC):
    def __init__(self, description, amount):
        self.description = description
        self.amount = float(amount)

    @abstractmethod
    def get_amount(self):
        pass

class IncomeEntry(Entry):
    def get_amount(self):
        return self.amount

class ExpenseEntry(Entry):
    def get_amount(self):
        return self.amount



class BudgetManager:
    def __init__(self):
        self.incomes = []
        self.expenses = []

    def add_income(self, entry: IncomeEntry):
        self.incomes.append(entry)

    def add_expense(self, entry: ExpenseEntry):
        self.expenses.append(entry)

    def get_total_income(self):
        return sum(i.get_amount() for i in self.incomes)

    def get_total_expense(self):
        return sum(e.get_amount() for e in self.expenses)

    def get_net_total(self):
        return self.get_total_income() - self.get_total_expense()



