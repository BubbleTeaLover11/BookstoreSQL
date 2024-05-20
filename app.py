from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os

app = Flask(__name__)

app.config["MYSQL_HOST"] = "classmysql.engr.oregonstate.edu"
app.config["MYSQL_USER"] = "cs340_chenwill"
app.config["MYSQL_PASSWORD"] = "JeuYwPY70IXx"
app.config["MYSQL_DB"] = "cs340_chenwill"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"


mysql = MySQL(app)


# Routes
@app.route('/')
def root():
    return render_template("main.j2")

@app.route('/orderdetails')
def orderdetails():
    query = "SELECT BookISBN, OID, OrderQty, UnitPrice, LineTotal FROM OrderDetails"
    cur = mysql.connection.cursor()
    cur.execute(query)
    order_details_result = cur.fetchall()
    return render_template("orderdetails.j2", order_details = order_details)

@app.route('/createorderdetails')
def create_order_detail():
    if not BookISBN and not OID:
        return redirect("/orderdetails")
    if not BookISBN:
        query = "INSERT INTO OrderDetails (OID, OrderQty, UnitPrice, LineTotal) VALUES (%s, 0, 0, 0)"
        cur = mysql.connection.cursor()
        cur.execute(query, (OID, OrderQty, UnitPrice, LineTotal))
        mysql.connection.commit()
    elif not OID:
        query = "INSERT INTO OrderDetails (BookISBN, OrderQty, UnitPrice, LineTotal) VALUES (%s, %s, (SELECT Price FROM Books WHERE BookISBN = BookISBN), UnitPrice * LineTotal)"
        cur = mysql.connection.cursor()
        cur.execute(query, (OID, OrderQty, UnitPrice, LineTotal))
        mysql.connection.commit()  
    else:
        query = "INSERT INTO OrderDetails (BookISBN, OID, OrderQty, UnitPrice, LineTotal) VALUES (%s, %s, %s, (SELECT Price FROM Books WHERE BookISBN = BookISBN), UnitPrice * LineTotal)"
        cur = mysql.connection.cursor()
        cur.execute(query, (OID, OrderQty, UnitPrice, LineTotal))
        mysql.connection.commit()
    return redirect("/orderdetails")
    

# Listener
if __name__ == "__main__":

    #Start the app on port 3000, it will be different once hosted
    app.run(port = 9001, debug = True)