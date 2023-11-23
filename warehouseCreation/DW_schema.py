olistdw_Customerdim_table = """
IF object_id('Customerdim') is null
CREATE TABLE Customerdim (
customer_id VARCHAR(100) PRIMARY KEY,
customer_unique_id VARCHAR (100) NOT NULL,
customer_zip_code_prefix INT,
customer_city VARCHAR(50),
customer_state VARCHAR(50)
);
"""

olistdw_Productdim_table = """
IF object_id('Productdim') is null
CREATE TABLE Productdim (
product_id VARCHAR(100) PRIMARY KEY,
product_category_name VARCHAR(200),
product_photos_qty FLOAT(50),
product_weight_g FLOAT(50),
product_length_cm FLOAT(50),
product_height_cm FLOAT(50),
product_width_cm FLOAT(50) 
);
"""

olistdw_Sellerdim_table = """
IF object_id('Sellerdim') is null
CREATE TABLE Sellerdim (
seller_id VARCHAR(100) PRIMARY KEY,
seller_zip_code_prefix INT,
seller_city VARCHAR(50),
seller_state VARCHAR(50)
);
"""

olistdw_PaymentTypedim_table = """
IF object_id('PaymentTypedim') is null
CREATE TABLE PaymentTypedim (
payment_type_id INT PRIMARY KEY,
payment_type VARCHAR(50) 
);
"""

olistdw_Datedim_table = """
IF object_id('Datedim') is null
CREATE TABLE Datedim (
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

olistdw_OrderFact_table = """
IF object_id('OrderFact') is null
CREATE TABLE OrderFact (
order_id VARCHAR(100) PRIMARY KEY,
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
FOREIGN KEY (order_id) REFERENCES OrderFact(order_id),
FOREIGN KEY (customer_id) REFERENCES Customerdim(customer_id),
FOREIGN KEY (product_id) REFERENCES Productdim(product_id),
FOREIGN KEY (seller_id) REFERENCES Sellerdim(seller_id),
FOREIGN KEY (payment_type_id) REFERENCES PaymentTypedim(payment_type_id)
);
"""

olistdw_OrderDateFact_table = """
IF object_id('OrderDateFact') is null
CREATE TABLE OrderDateFact (
order_id VARCHAR(100) 
order_purchase_timestamp_key DATETIME,
order_approved_at_key DATETIME,
order_delivered_carrier_date_key DATETIME,
order_delivered_customer_date_key DATETIME,
order_estimated_delivery_date_key DATETIME,
FOREIGN KEY (order_id)
REFERENCES OrderFact(order_id)
FOREIGN KEY (order_purchase_timestamp_key,order_approved_at_key,order_delivered_carrier_date_key, order_delivered_customer_date_key, order_estimated_delivery_date_key)
REFERENCES OrderFact(DateKey)
);
"""

olistdw_Reviewdim_table= """
IF object_id('Reviewdim') is null
CREATE TABLE Reviewdim (
order_id VARCHAR(100),
review_score INT,
review_comment_title VARCHAR(1000),
review_comment_message VARCHAR(8000),
review_creation_date DATETIME,
review_answer_timestamp DATETIME,
FOREIGN KEY (order_id)
REFERENCES OrderFact(order_id)
);
"""