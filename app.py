from flask import Flask, render_template, abort, request, redirect, url_for, flash, session
from Models import *
from format import format_price, isNumeric


app = Flask(__name__)
app.secret_key= "my_secret_key"

app.jinja_env.filters["format_total"] = format_price

BUDGET = 500

@app.route("/",methods=["GET","POST"])
def Homepage():

    if "expenses" not in session:
        session["expenses"] = []

    if "incomes" not in session:
        session["incomes"] = []


    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        formType = request.form.get("action")
        if formType == "reset":
            return reset()
        if formType == "addExpense":
            ExpenseDecsription = request.form.get("expenseDescription")
            ExpenseAmount = request.form.get("expense")


            if not isNumeric(ExpenseAmount):
                flash("Expense amount must be numeric")
                return redirect(url_for("Homepage"))
            ExpenseAmount = round(float(ExpenseAmount), 2)

            session["expenses"].append({"description": ExpenseDecsription,
                                            "amount": ExpenseAmount})
            session.modified = True

        if formType == "addIncome":
            IncomeDescription = request.form.get("incomeDescription")
            IncomeAmount = request.form.get("amount")

            if not isNumeric(IncomeAmount):
                flash("Income amount must be numeric")
                return redirect(url_for("Homepage"))

            IncomeAmount = round(float(IncomeAmount), 2)

            session["incomes"].append({"description": IncomeDescription,
                                            "amount": IncomeAmount})

            session.modified = True
    return render_template("index.html")

@app.route("/summary")
def Summary():

    incomes = session.get("incomes", [])
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
                           net_total=manager.get_net_total(),
                           budget = BUDGET
                           )




def reset():
    session.clear()
    return redirect(url_for("Homepage"))

@app.errorhandler(404)
def page_not_found(error):
    return render_template("page_not_found.html")




if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)