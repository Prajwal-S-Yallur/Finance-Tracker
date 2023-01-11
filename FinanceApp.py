import datetime
import pytz
# Basic Flask imports
from flask import Flask, redirect, render_template, request, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# Import from your custom module
from FinanceDB.SetupDB import Finance

# Connect to the database
engine = create_engine("sqlite:///FinanceDB//finance_database.db")

# Initialize Flask
app = Flask(__name__)


@app.route("/finance")
def create_transaction():
    return render_template("create_transaction.html")


@app.route("/create_transaction", methods=["POST", "GET"])
def createTransaction():

    if request.method == "POST":
        # Get the data from the form and placed into a variable.
        input_data = request.form

        # A new session will have to be created in every function
        Session = sessionmaker(bind=engine)
        session = Session()

        # create a new transaction and enter it into the database
        new_transaction = Finance(
            transaction_date_time=datetime.datetime.strptime(
                input_data["transaction_date_time"], "%Y-%m-%dT%H:%M"
            )
            if input_data["transaction_date_time"]
            else pytz.timezone("Asia/Kolkata").localize(datetime.datetime.now()),
            transaction_name=input_data["transaction_name"],
            product_details=input_data["product_details"],
            product_seller=input_data["product_seller"],
            expenditure_category=input_data["expenditure_category"],
            expenditure_sub_category=input_data["expenditure_sub_category"],
            amount_spent=input_data["amount_spent"],
        )

        session.add(new_transaction)
        session.commit()
        session.close()
        return redirect(url_for("create_transaction"))

    else:
        return redirect(url_for("create_transaction"))


# Routing for simply reading the database (the 'R' in CRUD)
@app.route("/read_transactions")
def read():
    
    # Start this page's session
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Query all results from the database
    query = session.query(Finance).all()
    
    # render the template and pass the query into the html
    return render_template("read_transactions.html", query = query)
    

if __name__ == "__main__":
    app.run(debug=True, port=5000)
