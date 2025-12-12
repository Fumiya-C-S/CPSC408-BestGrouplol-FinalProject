# pylint: skip-file
#import MySQL
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from db_operations import db_operations
from helper import helper
import mysql.connector
from helper import helper
import random
#Make Connection
def get_db_connection():
        connection = mysql.connector.connect(host="localhost",
        user="root",
        password="CPSC408!",
        auth_plugin='mysql_native_password',
        database="DB_Project")
        try:
              yield connection
        finally:
              connection.close()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # our React web url
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get('/products/')
def get_product(db_ops = Depends(get_db_connection)):
    cursor = db_ops.cursor(dictionary = True)
    cursor.execute("Select* From Product")
    product_info = cursor.fetchall()
    cursor.close()
    return product_info
@app.get('/orders/')
def get_orders(db_ops = Depends(get_db_connection)):
    cursor = db_ops.cursor(dictionary = True)
    cursor.execute(f"Select* From users_order") # Query from the View
    orders_info = cursor.fetchall()
    cursor.close()
    return orders_info
@app.get('/users/')
def get_user(db_ops = Depends(get_db_connection)):
    cursor = db_ops.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Customer")
    product_info = cursor.fetchall()
    cursor.close()
    return product_info[0] if product_info else {}
@app.post('/create_view/')
def create_view(customer_id: str, db_ops = Depends(get_db_connection)):
    cursor = db_ops.cursor(dictionary=True)
    create_view = f'''
    CREATE VIEW users_order AS
    SELECT o.OrderID, o.OrderDate, o.Status
    FROM Orders AS o
    WHERE CustomerID = {customer_id};
    '''
    cursor.execute(create_view)
    db_ops.commit()
    cursor.close()
    return {"Result": "View was created"}
