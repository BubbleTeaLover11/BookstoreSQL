from flask import Flask, render_template, json
import os
import Step4.database.db_connector as db

# Configuration

app = Flask(__name__)
db_connection = db.connect_to_database()

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

# @app.route('/orders')
# def orders():
#     return render_template("orders.j2", orders = orders_from_app_py)

#debug = True will automatically refresh app so we don't have to keep rerun script
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3434))
    
    app.run(debug=True, port=port)