from sqlalchemy import create_engine,URL
import polars as pl
from data_extract import extraction
from data_transform import *


db_connection_string = r"Driver={ODBC Driver 17 for SQL Server};Server=tcp:192.168.0.104,1433;Database=olist;Uid=prasad;Pwd=Suraj123;TrustServerCertificate=yes;Connection Timeout=30;"
db_engine=create_engine(URL.create("mssql+pyodbc", query={"odbc_connect": db_connection_string}))

#have to create two engines for database(olist) and datawarehouse(olistDW) both
dw_connection_string = r"Driver={ODBC Driver 17 for SQL Server};Server=tcp:192.168.0.104,1433;Database=olistDW;Uid=prasad;Pwd=Suraj123;TrustServerCertificate=yes;Connection Timeout=30;"
dw_engine=create_engine(URL.create("mssql+pyodbc", query={"odbc_connect": dw_connection_string}))

with db_engine.connect() as conn:
    (customers_df, geolocation_df,
      order_items_df, order_payments_df, 
      order_reviews_df, orders_df, 
      products_df, sellers_df) = (extraction(conn).get_all_tables_data())
    
    #create dimension tables
    Productdim_df=create_Productdim(products_df)
    PaymentTypedim_df=create_PaymentTypedim(order_payments_df)
    Datedim_df=create_Datedim(orders_df)
    Reviewdim_df=create_Reviewdim(order_reviews_df)

    #create order_date_fact_df from order_df
    order_date_fact_df=create_OrderDateFact(orders_df)

   #customer_id already present in orders_df So no need to join the table
    joined_tables_df=orders_df.join(order_items_df,on="order_id",how="left")\
                          .join(Productdim_df,on="product_id",how="left")\
                          .join(sellers_df,on="seller_id",how="left")\
                          .join(order_payments_df,on="order_id",how="left")\
                          .join(PaymentTypedim_df,on="payment_type",how="left") 

    
    
