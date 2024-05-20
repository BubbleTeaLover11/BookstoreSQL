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
    query = "SELECT * FROM orderdetails;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("orderdetails.j2", order_details_results = results)

# Listener
if __name__ == "__main__":

    #Start the app on port 3000, it will be different once hosted
    app.run(port = 9001, debug = True)