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

# @app.route('/customers')
# def customers():
#     return render_template("customers.j2", customers = customers_from_app_py)

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
    
#Test

# Listener
if __name__ == "__main__":

    #Start the app on port 3000, it will be different once hosted
    app.run(port = 9001, debug = True)
# @app.route('/orders')
# def orders():
#     return render_template("orders.j2", orders = orders_from_app_py)

#debug = True will automatically refresh app so we don't have to keep rerun script
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3434))
    
    app.run(debug=True, port=port)