from sqlalchemy import create_engine,URL
from data_extract import *
from data_transform import *
from data_load import *
import DW_schema


#have to create two engines for database(olist) and datawarehouse(olistDW) both
db_connection_string = r"Driver={ODBC Driver 17 for SQL Server};Server=tcp:192.168.0.101,1433;Database=olist;Uid=prasad;Pwd=Suraj123;TrustServerCertificate=yes;Connection Timeout=30;"
db_engine=create_engine(URL.create("mssql+pyodbc", query={"odbc_connect": db_connection_string}))

dw_connection_string = r"Driver={ODBC Driver 17 for SQL Server};Server=tcp:192.168.0.101,1433;Database=olistDW;Uid=dwadmin;Pwd=Suraj123;TrustServerCertificate=yes;Connection Timeout=30;"
dw_engine=create_engine(URL.create("mssql+pyodbc", query={"odbc_connect": dw_connection_string}))

with db_engine.connect() as conn:
    (customers_df, geolocation_df,
      order_items_df, order_payments_df, 
      order_reviews_df, orders_df, 
      products_df, sellers_df) = (get_all_tables_data(conn))
    
    #create dimension tables
    Productdim_df=create_Productdim(products_df)
    PaymentTypedim_df=create_PaymentTypedim(order_payments_df)
    Datedim_df=create_Datedim(orders_df)
    Reviewdim_df=create_Reviewdim(order_reviews_df)

    #create order_date_fact_df from order_df
    order_date_fact_df=create_OrderDateFact(orders_df)
    #order_fact from dimension tables
    order_fact_df=create_OrderFact(orders_df,order_items_df,Productdim_df,
                                   sellers_df,order_payments_df,PaymentTypedim_df)
    
    print("All dataframes are created")
    conn.close()

#we use raw connection(DBAPI) to run DDL commands "with" context is not works well with raw connection
conn=dw_engine.raw_connection()
cursor=conn.cursor()
#create tables on datawarehouse
schema_dict=DW_schema.__dict__
#get table name if its not magic function as this dict always contains __dict__,__builtin__ kind of functions also
table_names=[table for table in schema_dict if (not table.startswith("__"))]
    
for table_name in table_names:
    query=schema_dict.get(table_name) #as raw query have \n we replace it
    cursor.execute(query)
conn.commit()
conn.close()
print("All tables created.")

with dw_engine.connect() as conn:
    #load transformed data to datawarehouse
    for table_name in table_names:
        match table_name:
            case "customerdim":  
                print(f"insert started for {table_name}")
                insert_data(table_name,customers_df,conn)
            case "productdim":
                print(f"insert started for {table_name}")
                insert_data(table_name,Productdim_df,conn)
            case "sellerdim":
                print(f"insert started for {table_name}")
                insert_data(table_name,sellers_df,conn)
            case "paymenttypedim":
                print(f"insert started for {table_name}")
                insert_data(table_name,PaymentTypedim_df,conn)
            case "datedim":
                print(f"insert started for {table_name}")
                insert_data(table_name,Datedim_df,conn)
            case "orderdatefact":
                print(f"insert started for {table_name}")
                insert_data(table_name,order_date_fact_df,conn)
            case "orderfact":
                print(f"insert started for {table_name}")
                insert_data(table_name,order_fact_df,conn)
            case "reviewdim":
                print(f"insert started for {table_name}")
                insert_data(table_name,Reviewdim_df,conn)
