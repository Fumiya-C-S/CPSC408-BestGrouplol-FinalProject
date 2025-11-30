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
    allow_origins=["http://localhost:5173"],  # your React dev server
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
def get_orders(customer_id: str, db_ops = Depends(get_db_connection)):
    cursor = db_ops.cursor(dictionary = True)
    cursor.execute(f"Select Orders.OrderDate, Total, Status From Orders Where Orders.CustomerID = {customer_id}")
    product_info = cursor.fetchall()
    cursor.close()
    return product_info
# query = '''
#          Select*
#          From Product
#         '''
# list = db_ops.select_query(query)
# print(list)
                        
#create cursor object
# startScreen()
# print(query)
# result = db_ops.select_query(query)
# for i in result:
#     print(i)
# for i in result:
#     print(i)
# # #create database schema
# # cur_obj.execute("CREATE SCHEMA RideShare;")
# #confirm execution worked by printing result
# cur_obj.execute("SHOW DATABASES;")
# for row in cur_obj:
#     print(row)
# #Print out connection to verify and close
# print(conn)
# db_ops.destructor()