from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

import datetime

# Import from your custom module
from FinanceDB.SetupDB import Finance

# Connect to the database
engine = create_engine("sqlite:///FinanceDB//finance_database.db")

# Basic Flask imports
from flask import Flask, request, redirect, url_for, render_template

# Initialize Flask
app = Flask(__name__)


@app.route("/finance")
def create_transaction():
    return render_template("create_transaction.html")


@app.route("/create_transaction", methods = ["POST", "GET"])
def createTransaction():
    
    if request.method == "POST":
        # Get the data from the form and placed into a variable. 
        input_data = request.form
        
        # A new session will have to be created in every function
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # create a new transaction and enter it into the database
        new_transaction = Finance(transaction_date_time = datetime.datetime.strptime(input_data["transaction_date_time"], '%Y-%m-%dT%H:%M'), transaction_name = input_data["transaction_name"], product_details = input_data["product_details"], product_seller = input_data["product_seller"], amount_spent = input_data["amount_spent"])
        session.add(new_transaction)
        session.commit()
        session.close()
        return redirect(url_for("create_transaction"))
    
    else:
        return redirect(url_for("create_transaction"))


if __name__ == '__main__':
    app.run(debug=True, port=5000)