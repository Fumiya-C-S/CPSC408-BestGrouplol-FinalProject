# Library Imports
import mysql.connector
import time
from datetime import date

mydb = mysql.connector.connect(
    host="fumiyas-macbook-pro-3.local",
    user="bestgrouphost",
    password="CPSC408!",
    database="eCommerce",
    auth_plugin='mysql_native_password'
    )

# Creating Cursor Object
cursor = mydb.cursor()

print("Connected")

# Creating the necessary tables for eCommerce Platform:
#------------------------------------------------------
# Create Customer Table:
create_customer_table = '''
CREATE TABLE Customer(
    CustomerID INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    Name VARCHAR(20),
    Address VARCHAR(30),
    Email VARCHAR(100)
);
'''
# cursor.execute(create_customer_table)

# Create Orders Table:
create_orders_table = '''
CREATE TABLE Orders(
    OrderID INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    OrderDate DATE,
    Total INT,
    Status VARCHAR(30),
    CustomerID INT,
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
);
'''
# cursor.execute(create_orders_table)

# Create Product Table:
create_product_table = '''
CREATE TABLE Product(
    ProductID INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    Name VARCHAR(500),
    Description VARCHAR(1024),
    Price Float,
    Category VARCHAR(225)
);
'''
# cursor.execute(create_product_table)

# Create ProductView Table:
create_product_view_table = '''
CREATE TABLE Product_View(
    ProductID INT NOT NULL ,
    CustomerID INT NOT NULL,
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID),
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
    PRIMARY KEY(ProductID, CustomerID)
);
'''
# cursor.execute(create_product_view_table)

# Create OrderItem Table:
create_cart_table = '''
CREATE TABLE Cart(
    CustomerID INT NOT NULL,
    ProductID INT NOT NULL ,
    Quantity INT,
    Price Float,
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID),
    PRIMARY KEY (CustomerID, ProductID)
);
'''
# cursor.execute(create_cart_table)

# Create Categories Table:
create_categories_table = '''
CREATE TABLE Categories(
    CategoriesID INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    ProductID INT NOT NULL,
    ParentCategory VARCHAR(50),
    Name VARCHAR(50),
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);
'''
# cursor.execute(create_categories_table)

# Create Inventory Table:
create_inventory_table = '''
CREATE TABLE Inventory(
    InventoryID INT NOT NULL,
    ProductID INT NOT NULL,
    Location VARCHAR(100),
    Quantity INT,
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID),
    PRIMARY KEY (InventoryID, ProductID)
);
'''
# cursor.execute(create_inventory_table)
#------------------------------------------------------
# Insert random rows into tables:
random_inserts = '''
INSERT INTO Product VALUES(1,'Signature Slim Solar+ wireless keyboard K980','Enjoy the magic of light with a wireless keyboard powered by solar and artificial light that’s always ready, rain or shine. Innovative Logi LightCharge energy management makes Signature Slim Solar+ so easy to keep charged, it’s like magic.',99.99,'Keyboard')
INSERT INTO Product VALUES(2,'Sony - WH-1000XM4 Wireless Noise-Cancelling Over-the-Ear Headphones - Midnight Blue', 'Sony’s intelligent noise canceling headphones with premium sound elevate your listening experience with the ability to personalize and control everything you hear. Get up to 30 hours of battery life with quick charging capabilities, enjoy an enhanced Smart Listening feature set, and carry conversations hands-free with speak-to-chat.',199.99,'Headphones')
INSERT INTO Product VALUES(3,'HP - 27" IPS LED FHD 100Hz Monitor with Adjustable Height (HDMI, VGA) - Silver & Black', 'When you need the right tech to take on a day full of projects, meetings, and more, you need the HP Series 5 27-inch FHD Height Adjust Monitor. Its sleek design complements any workspace. And its beautiful screen, adjustable stand, and comfort features take your productivity to the next level. Bring flexibility to the way you work through enhanced visual performance, contrast ratio, and refresh rate.',149.99,'Monitor')
INSERT INTO Categories VALUES(1,1,'Electronics','Keyboard');
INSERT INTO Categories VALUES(2,2,'Electronics','Headphones');
INSERT INTO Categories VALUES(3,3,'Electronics','Monitor');
INSERT INTO Inventory VALUES (1,1,'Texas',10);
INSERT INTO Inventory VALUES (2,2,'California',5);
INSERT INTO Inventory VALUES (3,3,'Califonria',50);
INSERT INTO Customer VALUES(1,'Miguel', '123 Chapman Ave.', 'mtellez@chapman.edu');
INSERT INTO Customer VALUES(2,'Fumi', '300 Murchison Dr.', 'shinagawa@chapman.edu');
INSERT INTO Customer VALUES(3,'Chris', '10904 Smash Center', 'chuy@chapman.edu');
INSERT INTO Product_View VALUES(1,1);
INSERT INTO Product_VIEW VALUES(2,2);
INSERT INTO Product_VIEW VALUES(3,3);
INSERT INTO Orders VALUES(1,NOW(), 13.99, 'Shipping', 1);
INSERT INTO Orders VALUES(2,NOW(), 140.00, 'Ordered', 2);
INSERT INTO Orders VALUES(3,NOW(), 34.89, 'Delivered', 3);
INSERT INTO Order_Item VALUES(1,1,2,199.98);
INSERT INTO Order_Item VALUES(2,1,1,99.99);
INSERT INTO Order_Item VALUES(3,3,1,34.89);
'''

# Iterate through each line of random_inserts:
# for line in random_inserts.splitlines():
#     cursor.execute(line)
#     mydb.commit()
#------------------------------------------------------

# STARTING QUERIES/FUNCTIONS TO BE CALLED FROM FRONTEND
# Queries for all tables

# Set list of existing tables:
existing_tables = {"Categories", "Customer", "Inventory", "Order_Item", "Orders", "Product", "Product_View"}

# Function that can retrieve all contents of a table, with the table name as the input
def get_table_contents(table_name):
    if table_name not in existing_tables:
        print("Enetered table does not exist... returning nothing")
        return

    # Query to get all contents
    get_table_contents_query = f'''
    SELECT *
    FROM {table_name};
    ''' 

    cursor.execute(get_table_contents_query)
    result = cursor.fetchall()
    print(result)

    return result

# Customer Table Queries:
def create_new_customer(name, address, email):

    create_new_customer_query = '''
    INSERT INTO Customer(name, address, email)
    VALUES (%s, %s, %s);
    '''

    cursor.execute(create_new_customer_query, (name, address, email))
    mydb.commit()

    print("Successfully created new customer record.")
    return

# Order Table Queries:
# Creates new order when customer purchases items
def create_new_order(customerID):
    # Obtain all items in cart for specific customer
    get_customer_cart_items = '''
    SELECT *
    FROM Cart
    WHERE CustomerID = %s;
    '''

    cursor.execute(get_customer_cart_items, list(customerID))
    cart_items = cursor.fetchall()

    # Variable to keep order total
    total = 0

    # Iterate through all items and obtain subtotal of each item, then add them to total
    for item in cart_items:
        item_quantity = item[2]
        # print("Quantity: ", item_quantity)
        item_price = item[3]
        # print("Price: ", item_price)

        subtotal = item_quantity * item_price
        total += subtotal

    # Obtain order's date
    today = date.today()
    # print(today)

    create_order = '''
    INSERT INTO Orders(OrderDate, Total, Status, CustomerID)
    VALUES(%s, %s, %s, %s)
    '''

    cursor.execute(create_order, (today, total, "Ordered", customerID))
    mydb.commit()

    # CALL FUNCTION THAT EDITS INVENTORY COUNTS !!!!!!

    print(cart_items)
    return

# Cart Table Queries:
# Add a new item into the cart for a specific customer
def add_to_cart(customerID, productID, quantity):
    # Get price of product
    get_product_price = '''
    SELECT Price
    FROM Product
    WHERE ProductID = %s;
    '''

    # Get price from returned query
    cursor.execute(get_product_price, list(productID))
    price = cursor.fetchone()
    price = price[0]


    add_item_to_cart = '''
    INSERT INTO Cart (CustomerID, ProductID, Quantity, Price)
    VALUES(%s, %s, %s, %s);
    '''

    cursor.execute(add_item_to_cart, (customerID, productID, quantity, price))
    mydb.commit()
    return

# Products Table Queries:
def create_new_product(name, description, price, category):
    create_new_product_query= '''
    INSERT INTO Product(Name, Description, Price, Category)
    VALUES(%s, %s, %s, %s);
    '''

    cursor.execute(create_new_product_query, (name, description, price, category))
    mydb.commit()

    print("Successfully added new product.")
    return

# Products View Table Queries:
def create_products_view(productID, customerID):
    add_product_viewed = '''
    INSERT INTO Product_View(ProductID, CustomerID)
    VALUES (%s, %s)
    '''

    cursor.execute(add_product_viewed, (productID, customerID))
    mydb.commit()
    print("Successfully Added A Product to a Customer's Viewed Products.")
    return


# Inventory Product Table Queries:

# Add a new inventory entry for a product at a location
def create_inventory_entry(inventoryID, productID, location, quantity):
    create_inventory_query = '''
    INSERT INTO Inventory (InventoryID, ProductID, Location, Quantity)
    VALUES (%s, %s, %s, %s);
    '''
    
    cursor.execute(create_inventory_query, (inventoryID, productID, location, quantity))
    mydb.commit()
    print("Successfully added new inventory entry.")
    return

# Update inventory quantity for a product (negative to decrease, positive to increase)
def update_inventory_quantity(productID, location, quantity_change):
    update_inventory_query = '''
    UPDATE Inventory
    SET Quantity = Quantity + %s
    WHERE ProductID = %s AND Location = %s;
    '''
    
    cursor.execute(update_inventory_query, (quantity_change, productID, location))
    mydb.commit()
    print(f"Successfully updated inventory for ProductID {productID}.")
    return

# Get all inventory locations and quantities for a specific product
def get_inventory_by_product(productID):
    get_inventory_query = '''
    SELECT Location, Quantity
    FROM Inventory
    WHERE ProductID = %s;
    '''
    
    cursor.execute(get_inventory_query, (productID,))
    result = cursor.fetchall()
    print(result)
    return result

# Decrease inventory quantities after an order is placed
def decrease_inventory_after_order(orderID):
    get_order_items_query = '''
    SELECT ProductID, Quantity
    FROM Order_Item
    WHERE OrderID = %s;
    '''
    
    cursor.execute(get_order_items_query, (orderID,))
    order_items = cursor.fetchall()
    
    for item in order_items:
        productID = item[0]
        quantity_ordered = item[1]

        decrease_query = '''
        UPDATE Inventory
        SET Quantity = Quantity - %s
        WHERE ProductID = %s
        LIMIT 1;
        '''
        
        cursor.execute(decrease_query, (quantity_ordered, productID))

    mydb.commit()
    print(f"Inventory updated for Order {orderID}.")
    return        

# def create_

# Categories Table Queries

# Add a new category entry for a product
def create_new_category(productID, parentCategory, name):
    create_category_query = '''
    INSERT INTO Categories (ProductID, ParentCategory, Name)
    VALUES (%s, %s, %s);
    '''
    
    cursor.execute(create_category_query, (productID, parentCategory, name))
    mydb.commit()
    print("Successfully added new category.")
    return

# Get all products in a specific category
def get_products_by_category(categoryName):
    get_by_category_query = '''
    SELECT p.ProductID, p.Name, p.Description, p.Price
    FROM Product p
    JOIN Categories c ON p.ProductID = c.ProductID
    WHERE c.Name = %s;
    '''
    
    cursor.execute(get_by_category_query, (categoryName,))
    result = cursor.fetchall()
    print(result)
    return result

# Get all products under a parent category
def get_products_by_parent_category(parentCategory):
    get_by_parent_query = '''
    SELECT p.ProductID, p.Name, p.Price, c.Name as SubCategory
    FROM Product p
    JOIN Categories c ON p.ProductID = c.ProductID
    WHERE c.ParentCategory = %s;
    '''
    
    cursor.execute(get_by_parent_query, (parentCategory,))
    result = cursor.fetchall()
    print(result)
    return result

# Add an item to an order
def add_order_item(orderID, productID, quantity):
    get_price_query = '''
    SELECT Price
    FROM Product
    WHERE ProductID = %s;
    '''
    
    cursor.execute(get_price_query, (productID,))
    price = cursor.fetchone()[0]
    total_price = price * quantity
    
    add_item_query = '''
    INSERT INTO Order_Item (OrderID, ProductID, Quantity, Price)
    VALUES (%s, %s, %s, %s);
    '''
    
    cursor.execute(add_item_query, (orderID, productID, quantity, total_price))
    mydb.commit()
    print("Successfully added item to order.")
    return

# Get all items in a specific order
def get_order_items(orderID):
    get_items_query = '''
    SELECT oi.ProductID, p.Name, oi.Quantity, oi.Price
    FROM Order_Item oi
    JOIN Product p ON oi.ProductID = p.ProductID
    WHERE oi.OrderID = %s;
    '''
    
    cursor.execute(get_items_query, (orderID,))
    result = cursor.fetchall()
    print(result)
    return result

# def create_new_category(productID, )


# Main Function (testing area)
# get_table_contents("Customer")
# create_new_customer("Jeffery", "999 Park Ave.", "bok@chapman.edu")
# add_to_cart("1", "3", 1)
# create_new_order("1")
# create_products_view("2", "1")


# Close all connections
cursor.close()
mydb.close()
print("Connections Closed!")

