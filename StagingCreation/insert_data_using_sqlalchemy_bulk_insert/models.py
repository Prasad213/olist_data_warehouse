import pandas as pd
from typing import Any, List, Optional
from sqlalchemy import Integer, String, FLOAT,DATETIME,VARCHAR,DECIMAL,REAL
from sqlalchemy.dialects.mssql import SMALLMONEY,DATETIME2
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from datetime import datetime
from sqlalchemy import ForeignKey

# declarative base class
class Base(DeclarativeBase):
    pass


class customers(Base):
    __tablename__ = "customers"
    customer_id:Mapped[str]=mapped_column(VARCHAR(100),primary_key=True)
    customer_unique_id:Mapped[str]=mapped_column(VARCHAR(100))
    customer_zip_code_prefix:Mapped[int]=mapped_column(Integer())
    customer_city:Mapped[str]=mapped_column(VARCHAR(50))
    customer_state:Mapped[str]=mapped_column(VARCHAR(50))

    def __init__(self,customer_id, customer_unique_id,customer_zip_code_prefix,customer_city,customer_state):
        self.customer_id=customer_id
        self.customer_unique_id=customer_unique_id
        self.customer_zip_code_prefix=customer_zip_code_prefix
        self.customer_city=customer_city
        self.customer_state=customer_state


class orders(Base):
    __tablename__ = "orders"
    order_id:Mapped[str]=mapped_column(VARCHAR(100),primary_key=True)
    customer_id:Mapped[str]=mapped_column(VARCHAR(100),ForeignKey("customers.customer_id"))
    order_status:Mapped[str]=mapped_column(VARCHAR(50))
    order_purchase_timestamp:Mapped[datetime]=mapped_column(DATETIME())
    order_approved_at:Mapped[datetime]=mapped_column(DATETIME())
    order_delivered_carrier_date:Mapped[datetime]=mapped_column(DATETIME())
    order_delivered_customer_date:Mapped[datetime]=mapped_column(DATETIME())
    order_estimated_delivery_date:Mapped[datetime]=mapped_column(DATETIME())

    def __init__(self,order_id,customer_id,order_status,order_purchase_timestamp,order_approved_at,order_delivered_carrier_date,order_delivered_customer_date,order_estimated_delivery_date):
        self.order_id=order_id
        self.customer_id=customer_id
        self.order_status=order_status
        self.order_purchase_timestamp=order_purchase_timestamp
        self.order_approved_at=order_approved_at
        self.order_delivered_carrier_date=order_delivered_carrier_date
        self.order_delivered_customer_date=order_delivered_customer_date
        self.order_estimated_delivery_date=order_estimated_delivery_date
        

class products(Base):
    __tablename__ = "products"
    product_id:Mapped[str]= mapped_column(VARCHAR(100),primary_key=True)
    product_category_name:Mapped[str]= mapped_column(VARCHAR(200))
    product_name_lenght:Mapped[float]=mapped_column(FLOAT(50))
    product_description_lenght:Mapped[float]=mapped_column(FLOAT(50))
    product_photos_qty:Mapped[float]=mapped_column(FLOAT(50))
    product_weight_g:Mapped[float]=mapped_column(FLOAT(50))
    product_length_cm:Mapped[float]=mapped_column(FLOAT(50))
    product_height_cm:Mapped[float]=mapped_column(FLOAT(50))
    product_width_cm:Mapped[float]=mapped_column(FLOAT(50))

    def __init__(self,product_id,product_category_name,product_name_lenght,product_description_lenght,product_photos_qty,product_weight_g,product_length_cm,product_height_cm,product_width_cm):
        self.product_id=product_id
        self.product_category_name=product_category_name
        self.product_name_lenght=product_name_lenght
        self.product_description_lenght=product_description_lenght
        self.product_photos_qty=product_photos_qty
        self.product_weight_g=product_weight_g
        self.product_length_cm=product_length_cm
        self.product_height_cm=product_height_cm
        self.product_width_cm=product_width_cm


class sellers(Base):
    __tablename__ = "sellers"
    seller_id:Mapped[str]=mapped_column(VARCHAR(200),primary_key=True)
    seller_zip_code_prefix:Mapped[int]=mapped_column(Integer())
    seller_city:Mapped[str]=mapped_column(VARCHAR(200))
    seller_state:Mapped[str]=mapped_column(VARCHAR(200))

    def __init__(self,seller_id,seller_zip_code_prefix,seller_city,seller_state):
        self.seller_id=seller_id
        self.seller_zip_code_prefix=seller_zip_code_prefix
        self.seller_city=seller_city
        self.seller_state=seller_state


class order_items(Base):
    __tablename__ = "order_items"
    order_item_id:Mapped[int]=mapped_column(Integer,primary_key=True,autoincrement=True)
    order_id:Mapped[str]=mapped_column(VARCHAR(100),ForeignKey("orders.order_id"))
    quantity:Mapped[int]=mapped_column(Integer)
    product_id:Mapped[str]=mapped_column(VARCHAR(100),ForeignKey("products.product_id"))
    seller_id:Mapped[str]=mapped_column(VARCHAR(100))
    shipping_limit_date:Mapped[datetime]=mapped_column(DATETIME(),nullable=True)
    price=mapped_column(SMALLMONEY())
    freight_value=mapped_column(SMALLMONEY())

    def __init__(self,order_id,order_item_id,product_id,seller_id,shipping_limit_date,price,freight_value):
        self.order_id=order_id
        self.order_item_id=order_item_id
        self.product_id=product_id
        self.seller_id=seller_id
        self.shipping_limit_date=shipping_limit_date
        self.price=price
        self.freight_value=freight_value


class order_payments(Base):
    __tablename__ = "order_payments"
    order_payments_id:Mapped[int]=mapped_column(Integer(),primary_key=True,autoincrement=True)
    order_id:Mapped[str]=mapped_column(VARCHAR(100),ForeignKey("orders.order_id"))
    payment_sequential:Mapped[int]=mapped_column(Integer())
    payment_type:Mapped[str]=mapped_column(VARCHAR(50))
    payment_installments:Mapped[int]=mapped_column(Integer())
    payment_value=mapped_column(SMALLMONEY())

    def __init__(self,order_id,payment_sequential,payment_type,payment_installments,payment_value):
        self.order_id=order_id
        self.payment_sequential=payment_sequential
        self.payment_type=payment_type
        self.payment_installments=payment_installments
        self.payment_value=payment_value


class order_reviews(Base):
    __tablename__ = "order_reviews"
    review_id:Mapped[int]=mapped_column(Integer,primary_key=True,autoincrement=True)
    order_id:Mapped[str]=mapped_column(VARCHAR(100),ForeignKey("orders.order_id"))
    review_score:Mapped[int]=mapped_column(Integer)
    review_comment_title:Mapped[str]=mapped_column(VARCHAR(5000),nullable=True)
    review_comment_message:Mapped[str]=mapped_column(VARCHAR(8000),nullable=True)
    review_creation_date:Mapped[datetime]=mapped_column(DATETIME(),nullable=True)
    review_answer_timestamp:Mapped[datetime]=mapped_column(DATETIME(),nullable=True)
    
    def __init__(self,review_id,order_id,review_score,review_comment_title,review_comment_message,review_creation_date,review_answer_timestamp):
        #self.review_id=review_id
        self.order_id=order_id
        self.review_score=review_score
        self.review_comment_title=review_comment_title
        self.review_comment_message=review_comment_message
        self.review_creation_date=review_creation_date
        self.review_answer_timestamp=review_answer_timestamp

class geolocation(Base):
    __tablename__ = "geolocation"
    geolocation_id:Mapped[int]=mapped_column(Integer,primary_key=True,autoincrement=True) #primary key is importatnt and no duplicates alllowed in primary key
    geolocation_zip_code_prefix: Mapped[int]=mapped_column(Integer) 
    geolocation_lat: Mapped[int]= mapped_column(REAL())
    geolocation_lng:Mapped[int]=mapped_column(REAL())
    geolocation_city: Mapped[str] = mapped_column(String(50))
    geolocation_state: Mapped[str]= mapped_column(String(50))

    def __init__(self,geolocation_zip_code_prefix,geolocation_lat,geolocation_lng,geolocation_city,geolocation_state):
        self.geolocation_zip_code_prefix=geolocation_zip_code_prefix
        self.geolocation_lat=geolocation_lat
        self.geolocation_lng=geolocation_lng
        self.geolocation_city=geolocation_city
        self.geolocation_state=geolocation_state