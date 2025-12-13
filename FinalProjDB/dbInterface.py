# pylint: skip-file
#import MySQL
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from db_operations import db_operations
from helper import helper
import mysql.connector
from helper import helper
import random

# Request models
class CartRemoveRequest(BaseModel):
    customer_id: int
    product_id: int
class CartAddRequest(BaseModel):
    customer_id: int
    product_id: int
    quantity: int

#Make Connection
def get_db_connection():
        connection = mysql.connector.connect(host="localhost",
        user="jeffery",
        password="CPSC408!",
        auth_plugin='mysql_native_password',
        database="eCommerce")
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
    cursor.execute("SELECT OrderID, OrderDate, Status, CustomerID FROM Orders")
    orders_info = cursor.fetchall()
    cursor.close()
    return orders_info

@app.get('/cart/{customer_id}')
def get_cart(customer_id: int, db_ops = Depends(get_db_connection)):
    cursor = db_ops.cursor(dictionary = True)
    query = '''
    SELECT c.CustomerID, c.ProductID, c.Quantity, c.Price,
           p.Name, p.Description
    FROM Cart c
    JOIN Product p ON c.ProductID = p.ProductID
    WHERE c.CustomerID = %s
    '''
    cursor.execute(query, (customer_id,))
    cart_info = cursor.fetchall()
    cursor.close()
    return cart_info

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
@app.post('/cart/add')
def add_to_cart(request: CartAddRequest, db_ops = Depends(get_db_connection)):
    cursor = db_ops.cursor(dictionary=True)
    
    # Get product price
    cursor.execute("SELECT Price FROM Product WHERE ProductID = %s", (request.product_id,))
    product = cursor.fetchone()
    
    if not product:
        cursor.close()
        raise HTTPException(status_code=404, detail="Product not found")
    
    price = product['Price']
    
    # Check if item already in cart
    cursor.execute(
        "SELECT * FROM Cart WHERE CustomerID = %s AND ProductID = %s",
        (request.customer_id, request.product_id)
    )
    existing = cursor.fetchone()
    
    if existing:
        # Update quantity
        cursor.execute(
            "UPDATE Cart SET Quantity = Quantity + %s WHERE CustomerID = %s AND ProductID = %s",
            (request.quantity, request.customer_id, request.product_id)
        )
    else:
        # Insert new item
        cursor.execute(
            "INSERT INTO Cart (CustomerID, ProductID, Quantity, Price) VALUES (%s, %s, %s, %s)",
            (request.customer_id, request.product_id, request.quantity, price)
        )
    
    db_ops.commit()
    cursor.close()
    
    return {"message": "Item added to cart"}
@app.post('/cart/remove')
def remove_from_cart(request: CartRemoveRequest, db_ops = Depends(get_db_connection)):
    cursor = db_ops.cursor(dictionary=True)
    cursor.execute(
        "DELETE FROM Cart WHERE CustomerID = %s AND ProductID = %s",
        (request.customer_id, request.product_id)
    )
    db_ops.commit()
    cursor.close()
    
    return {"message": "Item removed from cart"}