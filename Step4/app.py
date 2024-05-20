from flask import Flask, render_template, json, request
from flask_mysqldb import MySQL
import os
import database.db_connector as db

# Configuration

app = Flask(__name__)
db_connection = db.connect_to_database()

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_kimpatr'
app.config['MYSQL_PASSWORD'] = '6904' #last 4 of onid
app.config['MYSQL_DB'] = 'cs340_kimpatr'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)

# Example Data

customers_from_app_py = [
    {
        "FirstName" : "Patrick",
        "LastName" : "Kim",
        "Email" : "kimpatr@oregonstate.edu"
    },{
        "FirstName" : "William",
        "LastName" : "Chen",
        "Email" : "chenwill@oregonstate.edu"
    },{
        "FirstName" : "Jane",
        "LastName" : "Smith",
        "Email" : "jsmith@mail.com"
    }
 ]

orders_from_app_py = [
    {
        "Date" : "2024-03-23",
        "CustomerID" : 1
    },
    {
        "Date" : "2024-03-31",
        "CustomerID" : 2
    },
    {
        "Date" : "2024-04-02",
        "CustomerID" : 1
    },
    {
        "Date" : "2024-04-20",
        "CustomerID" : 3
    }
]
# Routes
@app.route('/')
def root():
    return render_template("main.j2")

# @app.route('/order-Details')
# def order_details():
#     query = "SELECT * FROM OrderDetails;"
#     cursor = db.execute_query(db_connection=db_connection, query=query)
#     results = cursor.fetchall()
#     return render_template("orderDetails.j2", OrderDetails=results)

@app.route('/orderdetails1', methods=["POST", "GET"])
def orderdetails():
    if request.method == "GET":
        query = "SELECT Books.ISBN, OrderDetails.OID, OrderDetails.OrderQty AS `Order Quantity`, OrderDetails.UnitPrice AS `Unit Price`, (OrderDetails.UnitPrice * OrderDetails.OrderQty) AS LineTotal FROM OrderDetails INNER JOIN Books ON OrderDetails.BookISBN = Books.ISBN ORDER BY OrderDetails.OID, Books.ISBN;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        
        # mySQL query to grab book ID/Title data for dropdown
        query2 = "SELECT ISBN, Title FROM Books"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        title_data = cur.fetchall()
        
        # render edit_orderDetails page passing our query data and title data to the edit_orderDetails template
        return render_template("orderDetails.j2", data=data, titles=title_data)
# @app.route('/customers')
# def customers():
#     return render_template("customers.j2", customers = customers_from_app_py)

# @app.route('/orders')
# def orders():
#     return render_template("orders.j2", orders = orders_from_app_py)

#debug = True will automatically refresh app so we don't have to keep rerun script
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3434))
    
    app.run(debug=True, port=port)