from flask import Flask, render_template, json, request, redirect
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

# Routes
@app.route('/')
def root():
    return render_template("main.j2")

@app.route('/orders', methods=["GET"])
def orders():
    query = "SELECT * FROM Orders"
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    
    # render edit_orderDetails page
    return render_template("orders.j2", data=data)

@app.route('/orderdetails', methods=["POST", "GET"])
def orderdetails():
    if request.method == "GET":
        query = "SELECT OrderDetails.ID, Books.ISBN, Books.Title, OrderDetails.OID, OrderDetails.OrderQty AS `Order Quantity`, OrderDetails.UnitPrice AS `Unit Price`, (OrderDetails.UnitPrice * OrderDetails.OrderQty) AS LineTotal FROM OrderDetails INNER JOIN Books ON OrderDetails.BookISBN = Books.ISBN ORDER BY OrderDetails.OID, Books.ISBN;"
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

# route to see customer Invoice    
@app.route('/orderdetails/<int:id>', methods=["GET"])
def custorderdetails(id):
    query = "SELECT Orders.ID, CONCAT(Customers.FirstName, ' ', Customers.LastName) AS FullName, CURDATE() AS CurrentDate FROM Customers INNER JOIN Orders ON Customers.ID = Orders.CID WHERE Orders.ID = %s" % (id)
    cur = mysql.connection.cursor()
    cur.execute(query)
    data1 = cur.fetchall()

    query2 = "SELECT Books.ISBN, Books.Title, OrderDetails.OrderQty, OrderDetails.UnitPrice, OrderDetails.LineTotal FROM OrderDetails INNER JOIN Books ON OrderDetails.BookISBN = Books.ISBN WHERE OrderDetails.OID = %s" % (id)
    cur = mysql.connection.cursor()
    cur.execute(query2)
    data2 = cur.fetchall()
    
    return render_template("custoderdetails.j2", headerdata=data1, bodydata=data2)

@app.route("/edit_orderdetails/<int:id>", methods=["POST","GET"])
def edit_orderdetails(id):
    if request.method == "GET":
        # query to grab info of order details with passed id
        query = "SELECT * FROM OrderDetails WHERE id = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        
        # query to grab book ID/Title data for dropdown
        query2 = "SELECT ISBN, Title FROM Books"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        title_data = cur.fetchall()
        
        # render edit_orderDetails page
        return render_template("edit_orderDetails.j2", data=data, titles=title_data)
    
    if request.method == "POST":
        if request.form.get("Edit_orderDetails"):
            # grab user form inputs
            ID = request.form["orderDetailsID"] # hidden
            ISBN = request.form["title"] # displays as title
            OID = request.form["OID"]
            OrderQty = request.form["OrderQty"]
            # UnitPrice = request.form["UnitPrice"] # hidden
            # LineTotal = request.form["LineTotal"] # hidden
            
            # Fetch UnitPrice from Books table based on ISBN
            query = "SELECT Price FROM Books WHERE ISBN = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (ISBN,))
            book = cur.fetchone()
            UnitPrice = book['Price']

            # Calculate LineTotal
            LineTotal = float(UnitPrice) * int(OrderQty)

            # no null inputs
            query = "UPDATE OrderDetails SET BookISBN = %s, OID = %s, OrderQty = %s, UnitPrice = %s, LineTotal = %s WHERE ID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (ISBN, OID, OrderQty, UnitPrice, LineTotal, ID))
            mysql.connection.commit()
            
            return redirect("/orderdetails")
#debug = True will automatically refresh app so we don't have to keep rerun script
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3434))
    
    app.run(debug=True, port=port)