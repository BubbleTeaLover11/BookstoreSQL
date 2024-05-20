from flask import Flask, render_template, json, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os
import Step4.database.db_connector as db

# Configuration

app = Flask(__name__)
db_connection = db.connect_to_database()

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

@app.route('/order-Details')
def order_details():
    query = "SELECT * FROM OrderDetails;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("orderDetails.j2", OrderDetails=results)
    # return results

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


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3434))
    
    app.run(debug=True, port=port)