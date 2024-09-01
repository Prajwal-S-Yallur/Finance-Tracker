import datetime
import pytz
import json
# Basic Flask imports
from flask import Flask, redirect, render_template, request, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# Import from your custom module
# from FinanceDB.SetupDB import Finance
from modules.sync_to_google_drive import authenticate_with_google_drive, upload_to_google_drive, create_folder
from modules.SetupDB import Finance
from modules.SetupDB import create_new_database
from modules.update_json_file import get_json_file_content, save_to_json_file
from modules.config import year, year_month, parent_folder_id, backup_folder_id

# Connect to the database
engine = create_engine("sqlite:///..//Data Base//Proudction//finance_database.db")

# Initialize Flask
app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route("/")
def on_start():
    return redirect(url_for("create_this_month_database"))



@app.route("/create_transaction", methods=["POST", "GET"])
def createTransaction():
    global engine

    if request.method == "POST":
        # Get the data from the form and placed into a variable.
        input_data = request.form

        # A new session will have to be created in every function
        Session = sessionmaker(bind=engine)
        session = Session()

        # create a new transaction and enter it into the database
        new_transaction = Finance(
            transaction_date_time = datetime.datetime.strptime(
                input_data["transaction_date_time"], "%Y-%m-%dT%H:%M"
            )
            if input_data["transaction_date_time"]
            else pytz.timezone("Asia/Kolkata").localize(datetime.datetime.now()),
            transaction_name = input_data["transaction_name"],
            product_details = input_data["product_details"],
            product_seller = input_data["product_seller"],
            expenditure_category = input_data["expenditure_category"],
            expenditure_sub_category = input_data["expenditure_sub_category"],
            amount_spent = input_data["amount_spent"],
        )

        session.add(new_transaction)
        session.commit()
        session.close()
        flash(f"Sucessfully Created New Transaction!")
        return redirect(url_for("read_transactions"))

    else:
        return render_template("create_transaction.html")


# Routing for simply reading the database (the 'R' in CRUD)
@app.route("/read_transactions", methods=["POST", "GET"])
def read_transactions():
    global engine

    # Start this page's session
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Query all results from the database
    query = session.query(Finance).all()
    
    session.close()
    # render the template and pass the query into the html
    return render_template("read_transactions.html", query = query)


# Routing for editing a transaction, including deletion (the 'U' and 'D' in CRUD)
@app.route("/transaction/<transaction_id>")
def edit(transaction_id):
    global engine

    # Start this page's session
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    
    # Query the transaction based on the id
    query = session.query(Finance).filter(Finance.transaction_id == transaction_id).one()    
    
    session.close()
    
    # Render the html with the query passed through it
    return render_template("edit_transaction.html", query = query)


# Routing to actually update the transaction
@app.route("/edit_transaction/<transaction_id>", methods = ["POST", "GET"])
def edit_transaction(transaction_id):
    global engine

    if request.method == "POST":
        # Get the data from the form and placed into a variable. 
        input_data = request.form
        
        # A new session will have to be created in every function
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        
        # Search for the transaction to change based on the transaction id
        query = session.query(Finance).filter(Finance.transaction_id == transaction_id).one()  
        
        # Write the changes to the database
        query.transaction_date_time = datetime.datetime.strptime(input_data["transaction_date_time"], "%Y-%m-%dT%H:%M")  if input_data["transaction_date_time"] else query.transaction_date_time
        query.transaction_name = input_data["transaction_name"]
        query.product_details = input_data["product_details"]
        query.product_seller = input_data["product_seller"]
        query.expenditure_category = input_data["expenditure_category"]
        query.expenditure_sub_category = input_data["expenditure_sub_category"]
        query.amount_spent = input_data["amount_spent"]
        session.commit()
        session.close()

        flash(f"Sucessfully Updated Transaction ID: {transaction_id}!")
        return redirect(url_for("read_transactions"))
    
    else:
        return redirect(url_for("read_transactions"))


# Routing for deleting a transaction
@app.route("/delete_transaction/<transaction_id>", methods = ["POST", "GET"])
def delete_transaction(transaction_id):
    global engine
    
    if request.method == "POST":
        
        # A new session will have to be created in every function
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        
        # Search for the transaction to change based on the transaction id
        query = session.query(Finance).filter(Finance.transaction_id == transaction_id).one()
        
        # Delete the row
        session.delete(query)
        session.commit()
        session.close()
        
        return redirect(url_for("read_transactions"))
        
    else:
        return redirect(url_for("read_transactions"))


@app.route("/update_cloud_database", methods=["POST", "GET"])
def update_cloud_database(is_empthy=False):
    global engine

    db_ref = get_json_file_content()
    
    # folder_id = "https://drive.google.com/drive/folders/1-q568zpzep_tX-kkdOJrnpYVjQ7nJyj0"  # Replace with the actual folder ID
    # folder_id = "1-q568zpzep_tX-kkdOJrnpYVjQ7nJyj0"  # Replace with the actual folder ID

    index = db_ref["years"].index(year)
    folder_ids = db_ref["year_folder_id"][index][year]

    if year_month in db_ref['months']:
        index = db_ref["months"].index(year_month)
        file_id = db_ref["months_details"][index][year_month]["file_details"]['id']
    else:
        file_id = None

    # new_folder_name = year_month

    backup_file_name = f'{pytz.timezone("Asia/Kolkata").localize(datetime.datetime.now()) :%Y-%m-%d %H:%M:%S}'
    # new_file_name = str(pytz.timezone("Asia/Kolkata").localize(datetime.datetime.now()))
    drive_service = authenticate_with_google_drive()
    response = upload_to_google_drive(drive_service, folder_ids['production']['id'], year_month, file_id)
    upload_to_google_drive(drive_service, folder_ids['backup']['id'], backup_file_name)

    flash("Upload Sucessfull!")
    flash(f"Uploaded file details: {response}")

    save_to_json_file(db_ref, response, details_of="file")
    if is_empthy:
        return
    return redirect(url_for("read_transactions"))


@app.route("/create_this_month_database", methods=["POST", "GET"])
def create_this_month_database():
    global engine
        
    year_month = f'{pytz.timezone("Asia/Kolkata").localize(datetime.datetime.now()) :%Y-%m}'
    # print("Year_Month:", year_month)
    monthly_new_db_file_path = f"sqlite:///..//Data Base//Production//{year_month}.db"
    # monthly_new_db_file_path = "sqlite:///..//Data Base//Production//finance_database.db"
    
    db_ref = get_json_file_content()

    flash(f"Json_file_content: {db_ref}")
    # flash(f"year_month's value: {year_month} and its type is {type(year_month)}")

    if year not in db_ref["years"]:
        print(f"Trying to create a Folder for: {year_month}")
        prod_response = create_folder(year, parent_folder_id)
        backup_response = create_folder(year, backup_folder_id)
        response = {'production': prod_response, 'backup': backup_response}
        save_to_json_file(db_ref, response, details_of="folder")

    if year_month not in db_ref["months"]:
        print(f"Trying to create DB for: {year_month}")
        create_new_database(monthly_new_db_file_path)
        # response = create_folder(year_month, parent_folder_id)

        # save_to_json_file(db_ref, response, details_of="folder")
        
        flash(f"Sucessfully Created New Database for month: {year_month}!")
    else:
        flash(f"Already There is a Database for month: {year_month}!")
        flash(f"Now you are viewing the Database for month: {year_month} in this page!")
    # A new session will have to be created in every function
    engine = create_engine(monthly_new_db_file_path)
    
    return redirect(url_for("read_transactions"))
    

    # else:
    #     return render_template("create_transaction.html")
    

if __name__ == "__main__":
    app.run(debug=True, port=5000)
