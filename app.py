from flask import Flask, render_template, json, request, redirect
from flask_mysqldb import MySQL
import os
import database.db_connector as db
from dotenv import load_dotenv, find_dotenv

# Configuration
load_dotenv(find_dotenv())

host =  os.environ.get("host")
user = os.environ.get("user")
passwd = os.environ.get("passwd")
database = os.environ.get("db")

app = Flask(__name__)
db_connection = db.connect_to_database(host = host, user = user, passwd = passwd, db = database)

app.config['MYSQL_HOST'] = host
app.config['MYSQL_USER'] = user
app.config['MYSQL_PASSWORD'] = passwd 
app.config['MYSQL_DB'] = database
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)

# Routes
@app.route('/')
def root():
    return render_template("main.j2")

@app.route('/books')
def books():
    # query = "SELECT * FROM Books"
    query = "SELECT Books.ISBN AS ISBN, Books.Title AS Title, Books.Genre AS Genre, Books.Stock AS Stock, Books.Price AS Price, CONCAT(Authors.FirstName, ' ', Authors.LastName) AS Author, Publishers.Company AS Publisher FROM Books INNER JOIN Authors ON Authors.ID = Books.AID INNER JOIN Publishers ON Publishers.ID = Books.PID"
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    
    return render_template("books.j2", data=data)

@app.route('/authors')
def authors():
    query = "SELECT * FROM Authors"
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    
    return render_template("authors.j2", data=data)

@app.route('/publishers')
def publishers():
    query = "SELECT * FROM Publishers"
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    
    return render_template("publishers.j2", data=data)

@app.route('/customers', methods=["GET"])
def customers():
    query = "SELECT * FROM Customers"
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    
    return render_template("customers.j2", data=data)

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

# route to see customer Invoice (for checking Links)
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
    
    return render_template("customerdetails.j2", headerdata=data1, bodydata=data2)

@app.route("/edit_orderdetails/<int:id>", methods=["POST","GET"])
def edit_orderdetails(id):
    if request.method == "GET":
        print("GET")
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
        ID = request.form["orderDetailsID"]
        ISBN = request.form["title"]
        OID = request.form["OID"]
        OrderQty = request.form["OrderQty"]
            
        if ISBN == "0" or OrderQty == "":
            return redirect("/orderdetails")

        # Fetch UnitPrice from Books table based on ISBN
        query = "SELECT Price FROM Books WHERE ISBN = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (ISBN,))
        book = cur.fetchone()
        UnitPrice = book['Price']

        print(UnitPrice, OrderQty)
        # Calculate LineTotal
        LineTotal = float(UnitPrice) * int(OrderQty)
        
        query2 = "UPDATE OrderDetails SET BookISBN = %s, OID = %s, OrderQty = %s, UnitPrice = %s, LineTotal = %s WHERE ID = %s"

        try:
            cur = mysql.connection.cursor()
            cur.execute(query2, (ISBN, OID, OrderQty, UnitPrice, LineTotal, ID))
            mysql.connection.commit()
            return redirect("/orderdetails")
        except:
            #Make an alert here or something
            return redirect("/orderdetails")
            

@app.route('/create-order-details', methods=["POST", "GET"])
def create_order():
    if request.method == "POST":
        ISBN = request.form["BookISBN"]
        OID = request.form["OrderID"]
        OrderQty = request.form["OrderQty"]
        price = f"(SELECT Price FROM Books WHERE ISBN = {ISBN})"
        curs = mysql.connection.cursor()
        curs.execute(price)

    if OID == '' and (ISBN == '' or ISBN == '0'):
        return redirect('/orderdetails')
    
    if ISBN == '0':
        query = f"INSERT INTO OrderDetails (BookISBN, OID, OrderQty, UnitPrice, LineTotal) VALUES (NULL, {OID}, {OrderQty}, 0, 0);"
    elif OID == "":
        query = f"INSERT INTO OrderDetails (BookISBN, OID, OrderQty, UnitPrice, LineTotal) VALUES ({ISBN}, NULL, {OrderQty}, {price}, {price} * OrderQty);"
    else:
        query = f"INSERT INTO OrderDetails (BookISBN, OID, OrderQty, UnitPrice, LineTotal) VALUES ({ISBN}, {OID}, {OrderQty}, {price}, {price} * {OrderQty});"

    try:    
        curs = mysql.connection.cursor()
        curs.execute(query)
        mysql.connection.commit()
        return redirect('/orderdetails')
    except:
        return redirect('/orderdetails')
        
    
@app.route('/delete-order-details/<int:id>')
def delete_order_details(id):
    query = f"DELETE FROM OrderDetails WHERE ID = {id}"
    cur = mysql.connection.cursor()
    cur.execute(query)
    
    query2 = f"DELETE FROM Orders WHERE NOT EXISTS (SELECT OID From OrderDetails);"
    cur = mysql.connection.cursor()
    cur.execute(query2)
    mysql.connection.commit()

    return redirect('/orderdetails')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5809))
    app.run(debug=True, port=port)