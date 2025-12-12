# Library Imports
import mysql.connector
import pandas as pd
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

# Create Product-Category Table for M-M Relationship
create_product_category = '''
CREATE TABLE ProductCategory(
    ProductID  INT NOT NULL,
    CategoriesID INT NOT NULL,
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID),
    FOREIGN KEY (CategoriesID) REFERENCES Categories(CategoriesID),
    PRIMARY KEY (ProductID, CategoriesID)
);
'''
# cursor.execute(create_product_category)

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
INSERT INTO Cart VALUES(1,1,2,199.98);
INSERT INTO Cart VALUES(2,1,1,99.99);
INSERT INTO Cart VALUES(3,3,1,34.89);
'''

additional_random_inserts = '''
INSERT INTO Orders VALUES(7, NOW(), 80.00, 'Ordered', 2);
INSERT INTO Orders VALUES(5, NOW(), 255.00, 'Ordered', 2);
INSERT INTO Orders VALUES(6, NOW(), 34.89, 'Shipping', 3);
INSERT INTO Product VALUES(4, 'Alienware 27 Gaming Monitor - AW2725DM','Bring your favorite games to life in a 27” QHD gaming monitor featuring a Fast IPS panel, vivid color and smooth visuals.', 179.99,'Monitor')
INSERT INTO Product VALUES(5, 'G SERIES G703 LIGHTSPEED Wireless Gaming Mouse', 'Featuring the advanced HERO 25K gaming sensor for sub-micron tracking and 10x power efficiency over previous generation. Pro-grade LIGHTSPEED wireless delivers ultralow-latency for peak performance.',59.99,'Mouse')
INSERT INTO Product VALUES(6, 'G SERIES G840 Extra-Large Cloth Gaming Mouse Pad', 'Full desktop gaming mouse pad with space to configure your setup the way you want. Surface texture is performance-tuned for Logitech G mice. Rubber base stays in place for focus and control in-game.',39.99,'Mouse Pad')
'''

# Queries to add is_deleted column to tables
add_is_deleted = '''
ALTER TABLE Customer ADD COLUMN is_deleted BOOLEAN;
ALTER TABLE Orders ADD COLUMN is_deleted BOOLEAN;
ALTER TABLE Product ADD COLUMN is_deleted BOOLEAN;
ALTER TABLE Categories ADD COLUMN is_deleted BOOLEAN;
ALTER TABLE Inventory ADD COLUMN is_deleted BOOLEAN;
'''

additional_updating_queries = '''
ALTER TABLE Categories DROP CONSTRAINT categories_ibfk_1;
ALTER TABLE Categories DROP COLUMN ProductID;
ALTER TABLE Product DROP COLUMN Category;
INSERT INTO ProductCategory VALUES(1, 1);
INSERT INTO ProductCategory VALUES(2, 2);
INSERT INTO ProductCategory VALUES(3, 3);
INSERT INTO ProductCategory VALUES(4, 3);
'''

# RUN BELOW CODE CHUNK FOR UPDATED QUERIES
# Iterate through each line of random_inserts and additional_random_inserts:
# for line in random_inserts.splitlines():
#     cursor.execute(line)
#     mydb.commit()

# for line in additional_random_inserts.splitlines():
#     cursor.execute(line)
#     mydb.commit()

# Add is_deleted to all tables
# for line in add_is_deleted.splitlines():
#     cursor.execute(line)
#     mydb.commit()

# for line in additional_updating_queries.splitlines():
#     cursor.execute(line)
#     mydb.commit()

#------------------------------------------------------

# STARTING QUERIES/FUNCTIONS TO BE CALLED FROM FRONTEND
# Queries for all tables

# Set list of existing tables:
existing_tables = {"Categories", "Customer", "Inventory", "Cart", "Orders", "Product", "Product_View"}

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
    INSERT INTO Customer(name, address, email, is_deleted)
    VALUES (%s, %s, %s, 0);
    '''

    cursor.execute(create_new_customer_query, (name, address, email))
    mydb.commit()

    print("Successfully created new customer record.")
    return


def delete_customer_by_id(customerID):
    delete_customer_by_id = '''
    UPDATE Customer
    SET is_deleted = 1
    WHERE CustomerID = %s;
    '''

    cursor.execute(delete_customer_by_id, list(customerID))
    mydb.commit()
    return

# Function to recover customer by CustomerID
def recover_customer_by_id(customerID):
    recover_customer_by_id = '''
    UPDATE Customer
    SET is_deleted = 0
    WHERE CustomerID = %s;
    '''

    cursor.execute(recover_customer_by_id, list(customerID))
    mydb.commit()
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
    INSERT INTO Orders(OrderDate, Total, Status, CustomerID, is_deleted)
    VALUES(%s, %s, %s, %s, 0)
    '''

    cursor.execute(create_order, (today, total, "Ordered", customerID))
    mydb.commit()

    # CALL FUNCTION THAT EDITS INVENTORY COUNTS !!!!!!

    print(cart_items)
    return

# Process an order using transaction, if anything fails, rollback everything, creates an order from cart items and updates inventory atomically
def process_order_with_transaction(customerID):
    try:
        # Start transaction
        mydb.start_transaction()

        # Get cart items for customer
        get_cart_query = '''
        SELECT ProductID, Quantity, Price
        FROM Cart
        WHERE CustomerID = %s;
        '''
        cursor.execute(get_cart_query, (customerID,))
        cart_items = cursor.fetchall()

        if not cart_items:
            print("Cart is empty. No order created.")
            mydb.rollback()
            return None;

        # Calculate total
        total = sum(item[1] * item[2] for item in cart_items)

        # Create the order
        create_order_query = '''
        INSERT INTO Orders (OrderDate, Total, Status, CustomerID, is_deleted)
        VALUES (CURDATE(), %s, 'Ordered', %s, 0);
        '''
        cursor.execute(create_order_query, (total, customerID))
        orderID = cursor.lastrowid

        # Update invnetory for each item
        for item in cart_items:
            productID, quantity, price = item

            # Check inventory first
            check_inventory_query = '''
            SELECT SUM(Quantity) FROM Inventory
            WHERE ProductID = %s AND is_deleted = 0;
            '''
            cursor.execute(check_inventory_query, (productID,))
            inventory_result = cursor.fetchone()

            if inventory_result[0] is None or inventory_result[0] < quantity:
                # Not enough inventory, rollback everything
                mydb.rollback()
                print(f"Insufficient inventory for ProductID {productID}. Order cancelled.")
                return None

            # Decrease Inventory
            update_inventory_query = '''
            UPDATE Inventory
            SET Quantity = Quantity - %s
            WHERE ProductID = %s AND is_deleted = 0
            LIMIT 1;
            '''
            cursor.execute(update_inventory_query, (quantity, productID))

    # Clear cart
    clear_cart_query = '''
    DELETE FROM Cart WHERE CustomerID = %s;
    '''
    cursor.execute(clear_cart_query, (customerID,))

    # If everything succeeded, commit
    mydb.commit()
    print(f"Order {orderID} processed successfully!")
    return orderID

except Exception as e:
    # If any error occurs, rollback all changes
    mydb.rollback()
    print(f"Transaction failed: {e}. All changes rolled back.")
    return None


# Update specific order status to "Shipping"
def change_status_shipping(orderID):
    change_status = '''
    UPDATE Orders
    SET Status = "Shipping"
    WHERE OrderID = %s;
    '''

    cursor.execute(change_status, list(orderID))
    mydb.commit()
    return

def change_status_delivered(orderID):
    change_status = '''
    UPDATE Orders
    SET Status = "Delivered"
    WHERE OrderID = %s;
    '''

    cursor.execute(change_status, list(orderID))
    mydb.commit()
    return


# Function to delete an order by OrderID
def delete_order_by_id(orderID):
    delete_order = '''
    UPDATE Orders
    SET is_deleted = 1
    WHERE OrderID = %s;
    '''

    cursor.execute(delete_order, list(orderID))
    mydb.commit()
    return

# Function to recover an order by OrderID
def recover_order_by_id(orderID):
    recover_order = '''
    UPDATE Orders
    SET is_deleted = 0
    WHERE OrderID = %s;
    '''

    cursor.execute(recover_order, list(orderID))
    mydb.commit()
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

# Get all items in a specific order
def get_cart_items(orderID):
    get_items_query = '''
    SELECT oi.ProductID, p.Name, oi.Quantity, oi.Price
    FROM Cart oi
    JOIN Product p ON oi.ProductID = p.ProductID
    WHERE oi.OrderID = %s;
    '''
    
    cursor.execute(get_items_query, (orderID,))
    result = cursor.fetchall()
    print(result)
    return result

# Deletes an item from the cart or lower an product's quantity in cart (hard delete)
def delete_item_from_cart(customerID, productID, quantity):
    # First obtain quantity of product being deleted:
    get_product_quantity = '''
    SELECT Quantity
    FROM Cart
    WHERE CustomerID = %s AND ProductID = %s;
    '''

    cursor.execute(get_product_quantity, (customerID, productID))
    result = cursor.fetchone()

    # If product in cart doesn't exist:
    if result is None:
        print("Product not found in cart of the customer.")
        return
    
    current_quantity = result[0]

    # Check if item should be dropped or quantity to be decreased
    if result == quantity:
        # Drop row
        delete_item = '''
        DELETE FROM Cart
        WHERE CustomerID = %s AND ProductID = %s;
        '''

        cursor.execute(delete_item, (customerID, productID))
        mydb.commit()
        return
    else:
        # Decrease the quantity of the product in the cart
        decrease_quantity = '''
        UPDATE Cart
        SET quantity = %s
        WHERE CustomerID = %s AND ProductID = %s;
        '''

        decrease_amount = current_quantity - quantity
        cursor.execute(decrease_quantity, (decrease_amount, customerID, productID))
        mydb.commit()
        return

# Products Table Queries:
def create_new_product(name, description, price, category):
    create_new_product_query= '''
    INSERT INTO Product(Name, Description, Price, Category, is_deleted)
    VALUES(%s, %s, %s, %s, 0);
    '''

    cursor.execute(create_new_product_query, (name, description, price, category))
    mydb.commit()

    print("Successfully added new product.")
    return

# Delete product (soft delete)
def delete_product_by_id(productID):
    delete_product = '''
    UPDATE Product
    SET is_deleted = 1
    WHERE ProductID = %s;
    '''

    cursor.execute(delete_product, list(productID))
    mydb.commit()
    return

# Function to recover customer by CustomerID
def recover_product_by_id(productID):
    recover_product = '''
    UPDATE Product
    SET is_deleted = 0
    WHERE ProductID = %s;
    '''

    cursor.execute(recover_product, list(productID))
    mydb.commit()
    return

# Products View Table Queries:
# def create_products_view(productID, customerID):
#     add_product_viewed = '''
#     INSERT INTO Product_View(ProductID, CustomerID, is_deleted)
#     VALUES (%s, %s, 0)
#     '''

#     cursor.execute(add_product_viewed, (productID, customerID))
#     mydb.commit()
#     print("Successfully Added A Product to a Customer's Viewed Products.")
#     return


# Inventory Product Table Queries:
# Add a new inventory entry for a product at a location
def create_inventory_entry(inventoryID, productID, location, quantity):
    create_inventory_query = '''
    INSERT INTO Inventory (InventoryID, ProductID, Location, Quantity, is_deleted)
    VALUES (%s, %s, %s, %s, 0);
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
    get_cart_query = '''
    SELECT ProductID, Quantity
    FROM Cart
    WHERE OrderID = %s;
    '''
    
    cursor.execute(get_cart_query, (orderID,))
    cart_items = cursor.fetchall()
    
    for item in cart_items:
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

# Delete Inventory Item with ID (soft delete)
def delete_category_by_id(inventoryID, productID):
    delete_inventory = '''
    UPDATE Inventory
    SET is_deleted = 1
    WHERE InventoryID = %s AND ProductID = %s;
    '''

    cursor.execute(delete_inventory, (inventoryID, productID))
    mydb.commit()
    return

# Function to recover Inventory Ite, by inventoryID
def recover_category_by_id(inventoryID, productID):
    recover_inventory = '''
    UPDATE Inventory
    SET is_deleted = 0
    WHERE InventoryID = %s AND ProductID = %s;
    '''

    cursor.execute(recover_inventory, (inventoryID, productID))
    mydb.commit()
    return



# Categories Table Queries
# Add a new category entry for a product
def create_new_category(productID, parentCategory, name):
    create_category_query = '''
    INSERT INTO Categories (ProductID, ParentCategory, Name, is_deleted)
    VALUES (%s, %s, %s, 0);
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

# Delete category by category ID(soft_Delete)
def delete_category_by_id(categoryID):
    delete_category = '''
    UPDATE Category
    SET is_deleted = 1
    WHERE CategoriesID = %s;
    '''

    cursor.execute(delete_category, list(categoryID))
    mydb.commit()
    return

# Function to recover category by categoryID
def recover_category_by_id(categoryID):
    recover_category = '''
    UPDATE Category
    SET is_deleted = 0
    WHERE CategoriesID = %s;
    '''

    cursor.execute(recover_category, list(categoryID))
    mydb.commit()
    return

# Reports/Analytics 

# Get total sales 
def get_sales_by_category():
    sales_by_category_query = '''
    SELECT
        p.Category,
        COUNT(DISTINCT o.OrderID) AS TotalOrders,
        SUM(ca.Quantity) AS TotalUnitsSold,
        SUM(ca.Price) AS TotalRevenue
    FROM Cart ca
    JOIN Product p ON ca.ProductID = p.ProductID
    JOIN Customer c ON ca.CustomerID = c.CustomerID
    JOIN Orders o ON c.CustomerID = o.CustomerID
    GROUP BY p.Category
    ORDER BY TotalRevenue DESC;
    '''

    cursor.execute(sales_by_category_query)
    result = cursor.fetchall()
    print("Sales by Category:")
    for row in result:
        print(f"  {row[0]}: {row[1]} orders, {row[2]} units, ${row[3]:.2f} revenue")
    return result

# Get order count and total spending per customer
def get_customer_order_summary():
    customer_summary_query = '''
    SELECT 
        c.CustomerID,
        c.Name,
        COUNT(o.OrderID) AS NumberOfOrders,
        COALESCE(SUM(o.Total), 0) AS TotalSpent,
        AVG(o.Total) AS AverageOrderValue
    FROM Customer c
    LEFT JOIN Orders o ON c.CustomerID = o.CustomerID
    WHERE c.is_deleted = 0
    GROUP BY c.CustomerID, c.Name
    ORDER BY TotalSpent DESC;
    '''

    cursor.execute(customer_summary_query)
    result = cursor.fetchall()
    print("Customer Order Summary:")
    for row in result:
        print(f"  {row[1]}: {row[2]} orders, ${row[3]:.2f} total spent")
    return result

# Get total inventory value grouped by location
def get_inventory_summary_by_location():
    inventory_summary_query = '''
    SELECT 
        i.Location,
        COUNT(DISTINCT i.ProductID) AS NumberOfProducts,
        SUM(i.Quantity) AS TotalUnits,
        SUM(i.Quantity * p.Price) AS TotalInventoryValue
    FROM Inventory i
    JOIN Product p ON i.ProductID = p.ProductID
    WHERE i.is_deleted = 0
    GROUP BY i.Location
    ORDER BY TotalInventoryValue DESC;
    '''

    cursor.execute(inventory_summary_query)
    result = cursor.fetchall()
    print("Inventory by Location:")
    for row in result:
        print(f"  {row[0]}: {row[1]} products, {row[2]} units, ${row[3]:.2f} value")
    return result

# Get customers who spent more than average
def get_customers_with_above_average_spending():
    above_avg_query = '''
    SELECT c.CustomerID, c.Name, c.Email, SUM(o.Total) AS TotalSpent
    FROM Customer c
    JOIN Orders o ON c.CustomerID = o.CustomerID
    WHERE c.is_deleted = 0 AND o.is_deleted = 0
    GROUP BY c.CustomerID, c.Name, c.Email
    HAVING SUM(o.Total) > (
        SELECT AVG(Total) FROM Orders WHERE is_deleted = 0
    )
    ORDER BY TotalSpent DESC;
    '''

    cursor.execute(above_avg_query)
    result = cursor.fetchall()
    print("Customers with above-average spending:")
    for row in result:
        print(f"  {row[1]}: ${row[3]:.2f}")
    return result

# Get products that have never been in a cart
def get_products_never_ordered():
    never_ordered_query = '''
    SELECT ProductID, Name, Price, Category
    FROM Product
    WHERE is_deleted = 0 AND ProductID NOT IN (
        SELECT DISTINCT ProductID FROM Cart
    );
    '''
    
    cursor.execute(never_ordered_query)
    result = cursor.fetchall()
    print("Products never ordered:")
    for row in result:
        print(f"  {row[1]} (${row[2]:.2f})")
    return result

# Get products with inventory below threshold
def get_low_stock_products():
    low_stock_query = '''
    SELECT p.ProductID, p.Name, p.Category,
        (SELECT SUM(Quantity) FROM Inventory WHERE ProductID = p.ProductID) AS TotalStock
    FROM Product p
    WHERE p.is_deleted = 0
    HAVING TotalStock < 10 OR TotalStock IS NULL
    ORDER BY TotalStock ASC;
    '''

    cursor.execute(low_stock_query)
    result = cursor.fetchall()
    print("Low stock products:")
    for row in result:
        stock = row[3] if row[3] else 0
        print(f"  {row[1]}: {stock} units")
    return result

# Database Views & Indexes 

# Create database views
# Return VIEW of orders of a specific user (Only show orderID, orderDate, and shipping status):
def get_orders_for_id(userID):
    create_view = '''
    CREATE VIEW users_order AS
    SELECT o.OrderID, o.OrderDate, o.Status
    FROM Orders AS o
    WHERE CustomerID = %s;
    '''

    cursor.execute(create_view, list(userID))
    mydb.commit()
    return


# Export to Excel:
def export_excel_all_warehouse_inventory(output_file_name):
    get_all_inventory = '''
    SELECT p.ProductID, p.Name, SUM(i.Quantity) AS TotalQuantity
    FROM Inventory AS i
    INNER JOIN Product AS p
    ON i.ProductID = p.ProductID
    GROUP BY p.ProductID;
    '''

    results = pd.read_sql(get_all_inventory, mydb)

    results.to_excel(output_file_name)

    print(results)

    return results


# Add an item to an order
# def add_item_to_cart(orderID, productID, quantity):
#     get_price_query = '''
#     SELECT Price
#     FROM Product
#     WHERE ProductID = %s;
#     '''
    
#     cursor.execute(get_price_query, (productID,))
#     price = cursor.fetchone()[0]
#     total_price = price * quantity
    
#     add_item_query = '''
#     INSERT INTO Order_Item (OrderID, ProductID, Quantity, Price)
#     VALUES (%s, %s, %s, %s);
#     '''
    
#     cursor.execute(add_item_query, (orderID, productID, quantity, total_price))
#     mydb.commit()
#     print("Successfully added item to order.")
#     return


# Main Function (testing area)
# get_table_contents("Customer")
# create_new_customer("Jeffery", "999 Park Ave.", "bok@chapman.edu")
# add_to_cart("1", "3", 1)
# create_new_order("1")
# create_products_view("2", "1")
# get_orders_for_id("2")
# change_status_delivered("2")
export_excel_all_warehouse_inventory("test.xlsx")


# Close all connections
cursor.close()
mydb.close()
print("Connections Closed!")
