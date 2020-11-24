import decimal
from datetime import datetime
import mysql
from flask import request, session, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("mysql+pymysql://root:@localhost/expense")
db = scoped_session(sessionmaker(bind=engine))

def todict(listOfRow):
    rows=[row for row in listOfRow]

    return rows


def add_expenses(form, user_id):
    expenses=[]
    expense={"expense_type": request.form.get('expense_type'), "description": None, "amount": None, "date": None}

    for key, value in form:
        expense[key]=value.strip()

    expenses.append(expense)


    for expense in expenses:
        db.execute("INSERT INTO expenses (expense_type, description, amount, date, user_id) "
                   "VALUES(:expense_type, :description, :amount, :date,:user_id)",
                   {"expense_type": expense["expense_type"], "description": expense["description"], "amount": expense["amount"]
                    ,"date": datetime.now(), "user_id": user_id})
        db.commit()

        return expenses

def getHistory(userid):
    session.get("user_id")
    results = db.execute("SELECT expense_type, description, amount, date FROM `expenses` WHERE expenses.user_id=:user_id ",
                                    {"user_id": userid}).fetchall()
    return results


