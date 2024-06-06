# Citation for database.db_connector and adaptation
# Author: gkochera, et. al
# Date 6.4.2024
# Copied from https://github.com/osu-cs340-ecampus/flask-starter-app?tab=readme-ov-file
# Code for database.db_connector is used to connect to MySQL to provide functional Database usage
# Code from this website has been adapted and refitted for the purpose of this project

from flask import Flask, render_template, json, request, redirect, flash
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

#db_connection handles mySQL connection
#Code that handles CRUD operation is adapted from flask starter app
app = Flask(__name__)
db_connection = db.connect_to_database(host = host, user = user, passwd = passwd, db = database)

app.config['MYSQL_HOST'] = host
app.config['MYSQL_USER'] = user
app.config['MYSQL_PASSWORD'] = passwd 
app.config['MYSQL_DB'] = database
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)

# Routes

#INDEX
@app.route('/')
def root():
    return render_template("main.j2")

#BOOKS
@app.route('/books', methods=["POST", "GET"])
def books():
    # query = "SELECT * FROM Books"
    query = "SELECT Books.ISBN AS ISBN, Books.Title AS Title, Books.Genre AS Genre, Books.Stock AS Stock, Books.Price AS Price, CONCAT(Authors.FirstName, ' ', Authors.LastName) AS Author, Publishers.Company AS Publisher FROM Books INNER JOIN Authors ON Authors.ID = Books.AID INNER JOIN Publishers ON Publishers.ID = Books.PID ORDER BY ISBN asc"
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    
    aids = "SELECT ID, CONCAT(FirstName, ' ', LastName) as Name FROM Authors"
    pids = "SELECT ID, Company FROM Publishers"
    cur.execute(aids)
    aids = cur.fetchall()
    cur.execute(pids)
    pids = cur.fetchall()

    return render_template("books.j2", data=data, aids=aids, pids=pids)

@app.route('/create-book', methods=["POST", "GET"])
def create_book():

    if request.method == "POST":
        title = request.form['Title']
        genre = request.form['Genre']
        stock = request.form['Stock']
        price = request.form['Price']
        author = request.form['AID']
        publisher = request.form['PID']

        if author == '0' or publisher == '0':
            return redirect('/books')
        
        if int(stock) < 0:
            return redirect('/books')
        
        try:
            curs = mysql.connection.cursor()
            query = f"INSERT INTO Books (Title, Genre, Stock, Price, AID, PID) VALUES ('{title}', '{genre}', {stock}, {price}, {author}, {publisher}) "
            curs.execute(query)
            mysql.connection.commit()
        except:
            pass
        finally:
            return redirect("/books")

#AUTHORS
@app.route('/authors')
def authors():
    query = "SELECT * FROM Authors ORDER BY ID asc"
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    
    return render_template("authors.j2", data=data)

@app.route('/create-author', methods=["POST", "GET"])
def create_author():
    if request.method == "POST":
        fname = request.form["FirstName"]
        lname = request.form["LastName"]
        gender = request.form["Gender"]
        
        if gender == "":
            gender = "NULL"

        query = f"INSERT INTO Authors (FirstName, LastName, Gender) VALUES ('{fname}', '{lname}', '{gender}')"

        try:
            cur = mysql.connection.cursor()
            cur.execute(query)
            mysql.connection.commit()
        except:
            pass
        finally:
            return redirect('/authors')

#PUBLISHERS
@app.route('/publishers')
def publishers():
    query = "SELECT * FROM Publishers"
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    
    return render_template("publishers.j2", data=data)

@app.route('/create-publisher', methods=["POST", "GET"])
def create_publisher():
    if request.method == "POST":
        company = request.form['Company']
        year = request.form['Year']

        if company == "" or year == "":
            return redirect('/publishers')
        
        query = f"INSERT INTO Publishers (Company, Year) VALUES ('{company}', {year});"

        try:
            print(query)
            cur = mysql.connection.cursor()
            cur.execute(query)
            mysql.connection.commit()
            return redirect("/publishers")
        except:
            return redirect("/publishers")

#CUSTOMERS
@app.route('/customers', methods=["GET"])
def customers():
    query = "SELECT * FROM Customers"
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    
    return render_template("customers.j2", data=data)

@app.route('/create-customer', methods=["POST"])
def create_customer():
    if request.method == "POST":
        fname = request.form['FirstName']
        lname = request.form['LastName']
        email = request.form['Email']

    query = f'INSERT INTO Customers (FirstName, LastName, Email) VALUES ("{fname}", "{lname}", "{email}");'

    try:
        cur = mysql.connection.cursor()
        cur.execute(query)
        mysql.connection.commit()
    except:
        pass
    finally:
        return redirect('/customers')
    
@app.route('/edit-customer/<int:id>', methods=["POST", "GET"])
def edit_customer(id):
    cur = mysql.connection.cursor()

    if request.method == "GET":
        query = f"SELECT * FROM Customers WHERE id = {id}"
        cur.execute(query)
        data = cur.fetchall()

        return render_template("edit_customer.j2", data=data)
    
    if request.method == "POST":
        ID, fname, lname, email = request.form['ID'], request.form['fname'], request.form['lname'], request.form['email']

        query = f"UPDATE Customers SET FirstName='{fname}', LastName='{lname}', Email='{email}' WHERE ID={ID}"

        if fname == "" or lname == "" or email == "":
            return redirect('/customers')

        cur.execute(query)
        mysql.connection.commit()
        return redirect('/customers')
        
@app.route('/delete-customer/<int:id>')
def delete_customer(id):
    query = f'DELETE FROM Customers WHERE ID = {id}'
    cur = mysql.connection.cursor()
    cur.execute(query)
    mysql.connection.commit()

    return redirect('/customers')

#ORDERS
@app.route('/orders', methods=["GET"])
def orders():
    query = "SELECT Orders.ID AS OrderID, Date(Orders.Date), Orders.CID, CONCAT(Customers.FirstName, ' ', Customers.LastName) AS CustomerName FROM Orders INNER JOIN Customers ON Orders.CID = Customers.ID ORDER BY OrderID asc"
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    
    query2 = "SELECT * FROM Customers;"
    cur.execute(query2)
    cids = cur.fetchall()

    return render_template("orders.j2", data=data, cids=cids)

@app.route('/create-orders', methods=["POST"])
def create_orders():
    date = request.form['Date']
    CID = request.form['CID']

    query = f"INSERT INTO Orders (Date, CID) VALUES ('{date}', '{CID}');"

    if CID == "0":
        return redirect("/orders")
    
    try:
        curs = mysql.connection.cursor()
        curs.execute(query)
        mysql.connection.commit()
    except:
        pass
    finally:
        return redirect("/orders")

#ORDER DETAILS
@app.route('/orderdetails', methods=["POST", "GET"])
def orderdetails():
    if request.method == "GET":
        cur = mysql.connection.cursor()
        
        query = "SELECT OrderDetails.ID, Books.ISBN, Books.Title, OrderDetails.OID, OrderDetails.OrderQty AS `Order Quantity`, OrderDetails.UnitPrice AS `Unit Price`, (OrderDetails.UnitPrice * OrderDetails.OrderQty) AS LineTotal FROM OrderDetails INNER JOIN Books ON OrderDetails.BookISBN = Books.ISBN ORDER BY OrderDetails.OID, Books.ISBN;"
        cur.execute(query)
        data = cur.fetchall()
        
        # mySQL query to grab book ID/Title data for dropdown
        query2 = "SELECT ISBN, Title FROM Books"
        cur.execute(query2)
        title_data = cur.fetchall()
        
        # for OID drop down
        query3 = "SELECT * FROM Orders"
        cur.execute(query3)
        oid = cur.fetchall()
        
        print(oid[0]['Date'].month, oid[0]['Date'].day, oid[0]['Date'].year)
        # render edit_orderDetails page passing our query data and title data to the edit_orderDetails template
        return render_template("orderDetails.j2", data=data, titles=title_data, oid=oid)

# route to see customer Invoice (for checking Links)
@app.route('/orderdetails/<int:id>', methods=["GET"])
def custorderdetails(id):
    cur = mysql.connection.cursor()
    
    query = "SELECT Orders.ID, CONCAT(Customers.FirstName, ' ', Customers.LastName) AS FullName, CURDATE() AS CurrentDate FROM Customers INNER JOIN Orders ON Customers.ID = Orders.CID WHERE Orders.ID = %s" % (id)
    cur.execute(query)
    data1 = cur.fetchall()

    query2 = "SELECT Books.ISBN, Books.Title, OrderDetails.OrderQty, OrderDetails.UnitPrice, OrderDetails.LineTotal FROM OrderDetails INNER JOIN Books ON OrderDetails.BookISBN = Books.ISBN WHERE OrderDetails.OID = %s" % (id)
    cur.execute(query2)
    data2 = cur.fetchall()
    
    return render_template("customerdetails.j2", headerdata=data1, bodydata=data2)

@app.route("/edit-orderdetails/<int:id>", methods=["POST","GET"])
def edit_orderdetails(id):
    cur = mysql.connection.cursor()
    
    if request.method == "GET":
        # query to grab info of order details with passed id
        query = "SELECT * FROM OrderDetails WHERE id = %s" % (id)
        cur.execute(query)
        data = cur.fetchall()
        
        # query to grab book ID/Title data for dropdown
        query2 = "SELECT ISBN, Title FROM Books"
        cur.execute(query2)
        title_data = cur.fetchall()
        
        # for OID drop down
        query3 = "SELECT * FROM Orders"
        cur.execute(query3)
        oid = cur.fetchall()
        
        # render edit_orderDetails page
        return render_template("edit_orderDetails.j2", data=data, titles=title_data, oid=oid)
    
    if request.method == "POST":
        ID = request.form["orderDetailsID"]
        ISBN = request.form["title"]
        OID = request.form["OID"]
        OrderQty = request.form["OrderQty"]
            
        if ISBN == "0" or OrderQty == "":
            return redirect("/z")

        # Fetch UnitPrice from Books table based on ISBN
        query = "SELECT Price, Stock FROM Books WHERE ISBN = %s"
        cur.execute(query, (ISBN,))
        book = cur.fetchone()
        UnitPrice = book['Price']
        Stock = book['Stock']

        # Calculate LineTotal
        LineTotal = float(UnitPrice) * int(OrderQty)
        
        query2 = "UPDATE OrderDetails SET BookISBN = %s, OID = %s, OrderQty = %s, UnitPrice = %s, LineTotal = %s WHERE ID = %s"

        if int(OrderQty) > int(Stock):
            return redirect("/orderdetails")
        
        try:
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

    print(OID)

    if ISBN != '' and ISBN != '0':
        available = f"SELECT Stock FROM Books WHERE ISBN = {ISBN};"
        curs.execute(available)
        available = curs.fetchall()[0]['Stock']

    if OID == '' or (ISBN == '' or ISBN == '0') or int(OrderQty) < 1:
        return redirect('/orderdetails')

    if ISBN == '0':
        query = f"INSERT INTO OrderDetails (BookISBN, OID, OrderQty, UnitPrice, LineTotal) VALUES (NULL, {OID}, {OrderQty}, 0, 0);"
        curs.execute(query)
        mysql.connection.commit()
        return redirect('/orderdetails')
    elif int(OrderQty) > int(available):
        return redirect('/orderdetails')
    elif OID == "":
        query = f"INSERT INTO OrderDetails (BookISBN, OID, OrderQty, UnitPrice, LineTotal) VALUES ({ISBN}, NULL, {OrderQty}, {price}, {price} * OrderQty);"
    else:
        query = f"INSERT INTO OrderDetails (BookISBN, OID, OrderQty, UnitPrice, LineTotal) VALUES ({ISBN}, {OID}, {OrderQty}, {price}, {price} * {OrderQty});"

    try:    
        query2 = f"UPDATE Books SET Stock = {int(available) - int((OrderQty))} WHERE ISBN = {ISBN};"
        curs = mysql.connection.cursor()
        curs.execute(query)
        mysql.connection.commit()
        curs.execute(query2)
        mysql.connection.commit()
    except:
        pass
    finally:
        return redirect("/orderdetails")
          
@app.route('/delete-orderdetails/<int:id>')
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