import polars as pl

# class transformation():
#     def __init__(self,table_name,dataframe) -> None:
#         self.table_name=table_name
#         self.dataframe=dataframe

#     def transform(self):
#         match self.table_name:
#             case "Customerdim":  
#                 self.dataframe
#             case "Productdim":
#                 ...
#             case "Sellerdim":
#                 self.dataframe
#             case "PaymentTypedim":
#                 ...
#             case "Datedim":
#                 ...
#             case "OrderFact":
#                 ...
#             case "OrderDateFact":
#                 ...
#             case "Reviewdim":
#                 ... 

def create_Productdim(products_df):
    return products_df.drop(['product_category_name', 'product_name_lenght'])  
    
 #we can also use polars.DataFrame.with_row_count to add row count as id's    
def create_PaymentTypedim(order_payments_df):
    payment_type=order_payments_df.select("payment_type").unique() #take distinct values
    payment_id_df=pl.DataFrame({"payment_type_id": range(1,len(payment_type)+1)}) #create id dataframe
    PaymentTypedim_df=payment_id_df.with_columns(payment_type.select("payment_type")) #using with_columns add new column from other dataframe
    return PaymentTypedim_df

def create_Datedim(orders_df):  #provide order datframe to find range of dates in between orders are placed
    purchase_timestamp_df=orders_df.select("order_purchase_timestamp")
    min_date=purchase_timestamp_df.min()
    max_date=purchase_timestamp_df.max()
    start_date=str(min_date.select(pl.col("order_purchase_timestamp").dt.month_start().dt.date()).to_numpy()[0][0])
    end_date=str(max_date.select(pl.col("order_purchase_timestamp").dt.month_start().dt.date()).to_numpy()[0][0])
    from datetime import datetime
    #pl.expr.dt use for manipulate temporal data 
    date_range_df=pl.date_range(datetime.strptime(start_date,"%Y-%m-%d"),datetime.strptime(end_date,"%Y-%m-%d"),"1d",eager=True).to_frame("FullDate")
    date_df=date_range_df.select(pl.col("FullDate").dt.to_string("%d%m%Y").alias("DateKey"),
                                 pl.col("FullDate").dt.date(), #without alias function it take same column name
                                 pl.col("FullDate").dt.year().alias("Year"),
                                 pl.col("FullDate").dt.month().alias("MonthOfYear"),
                                 pl.col("FullDate").dt.to_string("%B").alias("MonthName"),
                                 pl.col("FullDate").dt.day().alias("DayOfMonth"),
                                 pl.col("FullDate").dt.weekday().alias("DayOfWeek"),
                                 pl.col("FullDate").dt.to_string("%A").alias("DayName"),
                                 pl.col("FullDate").dt.quarter().alias("Quarter")
                                 )
    return date_df

def create_Reviewdim(order_reviews_df):
    return order_reviews_df.drop("review_id")
 
def create_OrderFact(joined_tables_df):
    orders_fact_df=joined_tables_df.select(["order_id","customer_id","seller_id","product_id",
                                            "price","freight_value","quantity","payment_sequential",
                                            "payment_installments","payment_value","payment_type_id"])
    return orders_fact_df

def create_OrderDateFact(orders_df):
    order_date_fact_df=orders_df.select('order_id',
                                   pl.col('order_purchase_timestamp').dt.to_string("%d%m%Y").cast(pl.Int64).alias("order_purchase_timestamp_key"), 
                                   pl.col('order_approved_at').dt.to_string("%d%m%Y").cast(pl.Int64).alias("order_approved_at_key"), 
                                   pl.col('order_delivered_carrier_date').dt.to_string("%d%m%Y").cast(pl.Int64).alias("order_delivered_carrier_date_key"),
                                   pl.col('order_delivered_customer_date').dt.to_string("%d%m%Y").cast(pl.Int64).alias("order_delivered_customer_date_key"), 
                                   pl.col('order_estimated_delivery_date').dt.to_string("%d%m%Y").cast(pl.Int64).alias("order_estimated_delivery_date_key"))
    return order_date_fact_df





    