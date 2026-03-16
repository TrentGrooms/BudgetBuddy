from flask import Flask, render_template, abort, request, redirect, url_for, flash, session
from Models import *

app = Flask(__name__)
app.secret_key= "my_secret_key"

BUDGET = 500
@app.route("/",methods=["GET","POST"])
def Homepage():
    manager = BudgetManager()


    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        formType = request.form.get("action")
        if formType == "reset":
            reset()
        if formType == "addExpense":
            ExpenseDecsription = request.form.get("expenseDescription")
            ExpenseAmount = request.form.get("expense")
            expense = ExpenseEntry(ExpenseDecsription, ExpenseAmount)

            if "expenses" not in session:
                session["ExpenseList"] = manager.expenses
            else:
                session["ExpenseList"].append(expense)

        if formType == "addIncome":
            IncomeDescripton = request.form.get("incomeDescription")
            IncomeAmount = request.form.get("amount")
            income = IncomeEntry(IncomeDescripton, IncomeAmount)
            if "incomes" not in session:
                session["Incomes"] = manager.incomes
            else:
                session["Incomes"].append(income)
    return render_template("index.html")

@app.route("/summary")
def Summary():

    incomes = session.get("Incomes", [])
    expenses = session.get("expenses", [])

    manager = BudgetManager()

    for i in incomes:
        manager.add_income(IncomeEntry(i["description"], i["amount"]))

    session["TotalIncome"] = manager.get_total_income()

    for e in expenses:
        manager.add_expense(ExpenseEntry(e["description"], e["amount"]))
    session["TotalExpense"] = manager.get_total_expense()

    session["NetTotal"] = manager.get_net_total()


    return render_template("summary.html",
                           incomes=incomes,
                           expenses=expenses,
                           total_income=manager.get_total_income(),
                           total_expenses=manager.get_total_expense(),
                           net_total = manager.get_net_total(),
                           budget = BUDGET
                           )




def reset():
    session.clear()
    return redirect(url_for("/"))




if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)