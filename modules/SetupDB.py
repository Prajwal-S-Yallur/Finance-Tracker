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
    Base.metadata.create_all(engine)
