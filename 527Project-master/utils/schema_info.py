"""
This script is used for various schema related operations
"""

# below list stores the schemas names in application
schemas = ["aisles", "departments", "order_products", "users", "products", "orders"]

# below list stores the create queries for mysql
mysql_create_query = [
    """
    CREATE TABLE aisles
    (
        aisle_id INT NOT NULL,
        aisle VARCHAR(256) NOT NULL,
        department_id INT NOT NULL,
        PRIMARY KEY (aisle_id)
    )
    """,
    """
    CREATE TABLE departments
    (
        department_id INT NOT NULL,
        department VARCHAR(256) NOT NULL,
        PRIMARY KEY (department_id)
    )
    """,
    """
    CREATE TABLE users
    (
        user_id INT NOT NULL,
        PRIMARY KEY (user_id)
    )
    """,
    """
    CREATE TABLE order_products
    (
        product_id INT NOT NULL,
        order_id INT NOT NULL,
        add_to_cart_order INT NOT NULL,
        reordered INT NOT NULL
    )
    """,
    """
    CREATE TABLE orders
    (
        order_id INT NOT NULL,
        user_id INT NOT NULL,
        order_number INT NOT NULL,
        order_dow INT NOT NULL,
        order_hour_of_the_day INT NOT NULL,
        days_since_prior_order INT NOT NULL,
        PRIMARY KEY (order_id),
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    """,
    """
    CREATE TABLE products
    (
        aisle_id INT NOT NULL,
        product_id INT NOT NULL,
        product VARCHAR(256) NOT NULL,
        PRIMARY KEY (product_id),
        FOREIGN KEY (product_id) REFERENCES order_products(product_id),
        FOREIGN KEY (aisle_id) REFERENCES aisles(aisle_id)
    )
    """
]

# below list stores the schema and insert query map for insert in mysql
mysql_insert_map = {
    "aisles" : "insert into aisles(aisle_id, aisle, department_id) values(%s,%s,%s)",
    "departments" : "insert into departments(department_id, department) values(%s,%s)",
    "users" : "insert into users(user_id) values(%s)",
    "order_products" : "insert into order_products(order_id, product_id, add_to_cart_order, reordered) values(%s,%s,%s,%s)",
    "orders": "insert into orders(order_id, user_id, order_number, order_dow, order_hour_of_the_day, days_since_prior_order) values(%s,%s,%s,%s,%s,%s)",
    "products" : "insert into products(product_id, product, aisle_id) values(%s,%s,%s)"
}

