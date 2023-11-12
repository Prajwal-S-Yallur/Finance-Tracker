# Imports
import datetime

import pytz
from sqlalchemy import Column, DateTime, Float, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

# Pass a declarative base and create a object to correspond with a table in the database
Base = declarative_base()

class Finance(Base):

    __tablename__ = "finance"
    transaction_id = Column(Integer, primary_key=True)
    transaction_date_time = Column(
        DateTime(timezone=True),
        default=pytz.timezone("Asia/Kolkata").localize(datetime.datetime.now()),
        nullable=False,
    )
    transaction_name = Column(String(250), nullable=False)
    product_details = Column(String(250), nullable=False)
    product_seller = Column(String(250), nullable=False)
    expenditure_category = Column(String(250), nullable=False)
    expenditure_sub_category = Column(String(250), nullable=False)
    amount_spent = Column(Float, nullable=False)

def create_new_database(monthly_new_db_file_path):
    
    # Connect to and create the finance table
    engine = create_engine(monthly_new_db_file_path)
    # engine = create_engine(f"sqlite:///..//..//Data Base//Test//{month_file_name}.db")
    # engine = create_engine(f"sqlite:///..//Data Base//Test//{month_file_name}.db")
    # engine = create_engine("sqlite:///Data Base//Production//finance_database.db")
    Base.metadata.create_all(engine)

# # Start a session with the database
# Session = sessionmaker(bind=engine)
# session = Session()
# # # create a new finance and enter it into the database
# new_transaction = Finance(transaction_date_time = datetime.datetime.now(), transaction_name = "AI and Machine Learning for Coders", product_details = "AI and Machine Learning for Coders by Lorence Morony", product_seller = "Amazon", expenditure_category = "Learning & Development", expenditure_sub_category = "Technology - AI / ML / DL / DS", amount_spent = 1500)
# # # new_transaction = Finance(transaction_name = "AI and Machine Learning for Coders", product_details = "AI and Machine Learning for Coders by Lorence Morony", product_seller = "Amazon", expenditure_category = "Book", expenditure_sub_category = "Technology - AI / ML / DL / DS", amount_spent = 1500)
# session.add(new_transaction)
# session.commit()
