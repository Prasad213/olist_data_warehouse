#olist_dataset="""CREATE DATABASE olist;"""

olist_geolocation_dataset="""
IF OBJECT_ID(N'dbo.geolocation', N'U') IS NULL
CREATE TABLE geolocation (
geolocation_zip_code_prefix INT /*PRIMARY KEY*/,
geolocation_lat REAL,
geolocation_lng REAL,
geolocation_city VARCHAR(50),
geolocation_state VARCHAR(50)
);"""

olist_customers_dataset="""
IF OBJECT_ID(N'dbo.customers', N'U') IS NULL
CREATE TABLE customers (
customer_id VARCHAR(100) /*PRIMARY KEY*/,
customer_unique_id VARCHAR (100) NOT NULL,
customer_zip_code_prefix INT,
customer_city VARCHAR(50),
customer_state VARCHAR(50), 
/*FOREIGN KEY (customer_zip_code_prefix) REFERENCES geolocation(geolocation_zip_code_prefix)*/
);"""

olist_orders_dataset="""
IF OBJECT_ID(N'dbo.orders', N'U') IS NULL
CREATE TABLE orders(
order_id VARCHAR(100) /*PRIMARY KEY*/,
customer_id VARCHAR(100),
order_status VARCHAR(50),
order_purchase_timestamp DATETIME,
order_approved_at DATETIME,
order_delivered_carrier_date DATETIME,
order_delivered_customer_date DATETIME,
order_estimated_delivery_date DATETIME,
/*FOREIGN KEY (customer_id) REFERENCES customers(customer_id)*/
);"""

olist_products_dataset="""
IF OBJECT_ID(N'dbo.products', N'U') IS NULL
CREATE TABLE products(
product_id VARCHAR(100) /*PRIMARY KEY*/,
product_category_name VARCHAR(200),
product_name_lenght FLOAT(50),
product_description_lenght FLOAT(50),
product_photos_qty FLOAT(50),
product_weight_g FLOAT(50),
product_length_cm FLOAT(50),
product_height_cm FLOAT(50),
product_width_cm FLOAT(50)
);"""

olist_sellers_dataset="""
IF OBJECT_ID(N'dbo.sellers', N'U') IS NULL
CREATE TABLE sellers(
seller_id VARCHAR(max) /*PRIMARY KEY*/,
seller_zip_code_prefix INT,
seller_city VARCHAR(max),
seller_state VARCHAR(max),
/*FOREIGN KEY (seller_zip_code_prefix) REFERENCES sellers(geolocation_zip_code_prefix)*/
);"""


olist_order_items_dataset="""
IF OBJECT_ID(N'dbo.order_items', N'U') IS NULL
CREATE TABLE order_items (
order_id VARCHAR(100),
order_item_id INT,
product_id VARCHAR(100),
seller_id VARCHAR(100),
shipping_limit_date DATETIME,
price smallmoney,
freight_value smallmoney,
/*FOREIGN KEY (seller_id) REFERENCES sellers(seller_id),
FOREIGN KEY (product_id) REFERENCES products(product_id),
FOREIGN KEY (order_id) REFERENCES orders(order_id)*/
);"""
olist_order_payments_dataset="""
IF OBJECT_ID(N'dbo.order_payments', N'U') IS NULL
CREATE TABLE order_payments(
order_id VARCHAR(100),
payment_sequential INT,
payment_type VARCHAR(50),
payment_installments INT,
payment_value smallmoney,
/*FOREIGN KEY (order_id) REFERENCES orders(order_id)*/
);"""
olist_order_reviews_dataset="""
IF OBJECT_ID(N'dbo.order_reviews', N'U') IS NULL
CREATE TABLE order_reviews(
review_id VARCHAR(max) /*PRIMARY KEY*/,
order_id VARCHAR(100),
review_score INT,
review_comment_title VARCHAR(1000),
review_comment_message VARCHAR(8000),
review_creation_date DATETIME,
review_answer_timestamp DATETIME,
/*FOREIGN KEY (order_id) REFERENCES orders(order_id)*/
);"""

#drop commands        
"""drop table [dbo].[order_items];
drop table [dbo].[order_payments];
drop table [dbo].[order_reviews];
drop table [dbo].[orders];
drop table [dbo].[customers];
drop table [dbo].[geolocation];
drop table [dbo].[sellers];"""