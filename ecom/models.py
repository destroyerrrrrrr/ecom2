from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import pandas as pd
from . import db
import openpyxl

engine = create_engine("mysql://root:root@localhost/ecom")
Base = declarative_base()


# Creating the models
class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    category = db.Column(db.String(150), nullable=False)
    sub_category = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(150), nullable=False)
    img = db.Column(db.String(300))

# Saving the Excel data into MYSQL DB ...
wb = openpyxl.load_workbook(r'C:\Users\TQ823MU\Downloads\file_example_XLSX_50.xlsx')
df = pd.read_excel(r'C:\Users\TQ823MU\Downloads\file_example_XLSX_50.xlsx')
ws = wb['Sheet1']
column_names = [cell.value for cell in ws[1]]


class ExcelData(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    for column_name in column_names:
        exec(f'{column_name} = db.Column(db.String(255))')


# Create the table in the database
db.create_all()

# Create a session to manage database transactions
Session = sessionmaker(bind=engine)
session = Session()

for index, row in df.iterrows():
    new_row = ExcelData()
    for column_name in column_names:
        setattr(new_row, column_name, row[column_name])
        session.add(new_row)
session.commit()
