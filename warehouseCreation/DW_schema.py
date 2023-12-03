customerdim = """
IF object_id('customerdim') is null
CREATE TABLE customerdim (
customer_id VARCHAR(100) PRIMARY KEY,
customer_unique_id VARCHAR (100) NOT NULL,
customer_zip_code_prefix INT,
customer_city VARCHAR(50),
customer_state VARCHAR(50)
);
"""

productdim = """
IF object_id('productdim') is null
CREATE TABLE productdim (
product_id VARCHAR(100) PRIMARY KEY,
product_category_name VARCHAR(200),
product_photos_qty FLOAT(50),
product_weight_g FLOAT(50),
product_length_cm FLOAT(50),
product_height_cm FLOAT(50),
product_width_cm FLOAT(50) 
);
"""

sellerdim = """
IF object_id('sellerdim') is null
CREATE TABLE sellerdim (
seller_id VARCHAR(100) PRIMARY KEY,
seller_zip_code_prefix INT,
seller_city VARCHAR(50),
seller_state VARCHAR(50)
);
"""

paymenttypedim = """
IF object_id('paymenttypedim') is null
CREATE TABLE paymenttypedim (
payment_type_id INT PRIMARY KEY,
payment_type VARCHAR(50) 
);
"""

datedim = """
IF object_id('datedim') is null
CREATE TABLE datedim (
DateKey INT NOT NULL PRIMARY KEY,
FullDate DATETIME NOT NULL,
Year INT NOT NULL,
Quarter INT NOT NULL,
MonthOfYear INT NOT NULL,
MonthName varchar(15) NOT NULL,
DayOfMonth INT NOT NULL,
DayOfWeek INT NOT NULL,
DayName varchar(15) NOT NULL
);
"""
orderdatefact = """
IF object_id('orderdatefact') is null
CREATE TABLE orderdatefact (
order_id VARCHAR(100) PRIMARY KEY,
order_purchase_timestamp_key INT,
order_approved_at_key INT,
order_delivered_carrier_date_key INT,
order_delivered_customer_date_key INT,
order_estimated_delivery_date_key INT,
FOREIGN KEY (order_purchase_timestamp_key) REFERENCES datedim(DateKey),
FOREIGN KEY (order_approved_at_key) REFERENCES datedim(DateKey),
FOREIGN KEY (order_delivered_carrier_date_key) REFERENCES datedim(DateKey), 
FOREIGN KEY (order_delivered_customer_date_key) REFERENCES datedim(DateKey), 
FOREIGN KEY (order_estimated_delivery_date_key) REFERENCES datedim(DateKey)
);
"""

orderfact = """
IF object_id('orderfact') is null
CREATE TABLE orderfact (
order_id VARCHAR(100),
customer_id VARCHAR(100),
seller_id VARCHAR(100),
product_id VARCHAR(100),
price smallmoney,
freight_value smallmoney,
quantity INT,
payment_sequential INT,
payment_installments INT,
payment_value smallmoney,
payment_type_id INT,
FOREIGN KEY (order_id) REFERENCES orderdatefact(order_id),
FOREIGN KEY (customer_id) REFERENCES Customerdim(customer_id),
FOREIGN KEY (product_id) REFERENCES Productdim(product_id),
FOREIGN KEY (seller_id) REFERENCES Sellerdim(seller_id),
FOREIGN KEY (payment_type_id) REFERENCES PaymentTypedim(payment_type_id)
);
"""

reviewdim= """
IF object_id('reviewdim') is null
CREATE TABLE reviewdim (
order_id VARCHAR(100),
review_score INT,
review_comment_title VARCHAR(1000),
review_comment_message VARCHAR(8000),
review_creation_date DATETIME,
review_answer_timestamp DATETIME,
FOREIGN KEY (order_id)
REFERENCES orderdatefact(order_id)
);
"""