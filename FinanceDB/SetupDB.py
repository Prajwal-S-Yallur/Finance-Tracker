# Imports
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.sql import func
import datetime
import pytz

# Pass a declarative base and create a object to correspond with a table in the database
Base = declarative_base()
    
class Finance(Base):
    
    __tablename__ = 'finance'
    transaction_id = Column(Integer, primary_key=True)
    # transaction_date_time = Column(DateTime(timezone=True), default=pytz.timezone("Asia/Kolkata").localize(datetime.datetime.now()), nullable=False)
    transaction_name = Column(String(250), nullable=False)
    product_details = Column(String(250), nullable=False)
    # product_seller = Column(String(250), nullable=False)
    # expenditure_category = Column(String(250), nullable=False)
    # expenditure_sub_category = Column(String(250), nullable=False)
    amount_spent = Column(Float, nullable=False)


# Connect to and create the movie table
engine = create_engine("sqlite:///FinanceDB//finance_database.db")
# engine = create_engine("sqlite:///movies_database.db")
Base.metadata.create_all(engine)

# # Start a session with the database
# Session = sessionmaker(bind=engine)
# session = Session()
# # # create a new movie and enter it into the database
# new_transaction = Finance(transaction_name = "AI and Machine Learning for Coders", product_details = "AI and Machine Learning for Coders by Lorence Morony", amount_spent = 1500)
# # # new_transaction = Finance(transaction_name = "AI and Machine Learning for Coders", product_details = "AI and Machine Learning for Coders by Lorence Morony", product_seller = "Amazon", expenditure_category = "Book", expenditure_sub_category = "Technology - AI / ML / DL / DS", amount_spent = 1500)
# session.add(new_transaction)
# session.commit()