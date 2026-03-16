from flask import Flask, render_template, abort, request, redirect, url_for, flash, session
from Models import *

app = Flask(__name__)
app.secret_key= "my_secret_key"

@app.route("/")
def Homepage():
    manager = BudgetManager()


@app.route("/summary")
def Summary():
    None






if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)