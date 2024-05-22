
from flask import Flask, render_template, json, request, redirect
from flask_mysqldb import MySQL
import os
import database.db_connector as datab

app = Flask(__name__)
host = os.environ.get("340DBHOST")
user = os.environ.get("340DBUSER")
passwd = os.environ.get("340DBPW")
db = os.environ.get("340DB")
mysql = MySQL(app)

db_connection = datab.connect_to_database(host, user, passwd, db)

# Routes 

@app.route('/')
def root():
    return render_template("main.j2")

@app.route('/orderdetails', methods=["POST", "GET"])
def orderdetails():
    if request.method == "GET":
        query = "SELECT OrderDetails.ID, Books.ISBN, Books.Title, OrderDetails.OID, OrderDetails.OrderQty AS `Order Quantity`, OrderDetails.UnitPrice AS `Unit Price`, (OrderDetails.UnitPrice * OrderDetails.OrderQty) AS LineTotal FROM OrderDetails INNER JOIN Books ON OrderDetails.BookISBN = Books.ISBN ORDER BY OrderDetails.OID, Books.ISBN;"
        cursor = datab.execute_query(db_connection=db_connection, query=query)
        data = cursor.fetchall()
        
        # mySQL query to grab book ID/Title data for dropdown
        query2 = "SELECT ISBN, Title FROM Books"
        cursor = datab.execute_query(db_connection=db_connection, query=query2)
        cursor.execute(query2)
        title_data = cursor.fetchall()
        
        return render_template("orderDetails.j2", data=data, titles=title_data)

@app.route('/create-order-details', methods=["POST", "GET"])
def create_order():
    if request.method == "POST":
        ISBN = request.form["BookISBN"]
        OID = request.form["OrderID"]
        OrderQty = request.form["OrderQty"]

        if not OID and not ISBN:
            return redirect('/orderdetails')
        
        if not ISBN:
            query = f"INSERT INTO OrderDetails (BookISBN, OID, OrderQty, UnitPrice, LineTotal) VALUES (NULL, {OID}, {OrderQty}, 0, 0);"
        elif not OID:
            query = f"INSERT INTO OrderDetails (BookISBN, OID, OrderQty, UnitPrice, LineTotal) VALUES ({ISBN}, NULL, {OrderQty}, (SELECT Price FROM Books WHERE BookISBN = {ISBN}), (SELECT Price FROM Books WHERE BookISBN = {ISBN}) * OrderQty);"
        else:
            query = f"INSERT INTO OrderDetails (BookISBN, OID, OrderQty, UnitPrice, LineTotal) VALUES ({ISBN}, {OID}, {OrderQty}, (SELECT Price FROM Books WHERE BookISBN = {ISBN}), (SELECT Price FROM Books WHERE BookISBN = {ISBN}) * {OrderQty});"

        cursor = datab.execute_query(db_connection=db_connection, query=query)
        cursor.execute(query)

        return redirect('/orderdetails')
    
@app.route('/delete-order-details/<int:id>')
def delete_order_details(id):
    query = f"DELETE FROM OrderDetails WHERE ID = {id}"
    cur = mysql.connection.cursor()
    cur.execute(query)
    mysql.connection.commit()

    return redirect('/orderdetails')
        
        
    
@app.route('/orders', methods=["GET"])
def orders():
    query = "SELECT * FROM Orders"
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    
    # render edit_orderDetails page
    return render_template("orders.j2", data=data)

# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9112))
    print(host, user, passwd, db)
    app.run(port=port, debug=True)
