import polars as pl

def create_Productdim(products_df):
    return products_df.drop(['product_description_lenght', 'product_name_lenght'])  
    
 #we can also use polars.DataFrame.with_row_count to add row count as id's    
def create_PaymentTypedim(order_payments_df):
    payment_type=order_payments_df.select("payment_type").unique() #take distinct values
    payment_id_df=pl.DataFrame({"payment_type_id": range(1,len(payment_type)+1)}) #create id dataframe
    PaymentTypedim_df=payment_id_df.with_columns(payment_type.select("payment_type")) #using with_columns add new column from other dataframe
    return PaymentTypedim_df

def transform_to_datedim(dataframe):
    #pl.expr.dt use for manipulate temporal data
    date_df=dataframe.select(pl.col("FullDate").dt.to_string("%Y%m%d").cast(pl.Int64).alias("DateKey"),
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
def create_Datedim(orders_df):  #provide order datframe to find range of dates in between orders are placed
    # purchase_timestamp_df=orders_df.select("order_purchase_timestamp")
    # order_estimated_delivery_date=orders_df.select("order_estimated_delivery_date")
    # min_date=purchase_timestamp_df.min()
    # max_date=order_estimated_delivery_date.max()
    # start_date=str(min_date.select(pl.col("order_purchase_timestamp").dt.month_start().dt.date()).to_numpy()[0][0])
    # end_date=str(max_date.select(pl.col("order_estimated_delivery_date").dt.month_end().dt.date()).to_numpy()[0][0])
    from datetime import datetime,date
    start_date="2016-01-01"  
    end_date="2018-12-31"
    #we use this date because if order is processing or canceled this date is updated in delivered date fields
    excepted_date_df=pl.DataFrame({"FullDate":[datetime.strptime("1900-01-01","%Y-%m-%d")]})
    date_range_df=pl.date_range(datetime.strptime(start_date,"%Y-%m-%d"),datetime.strptime(end_date,"%Y-%m-%d"),"1d",eager=True).to_frame("FullDate")
    all_date_df=pl.concat([excepted_date_df,date_range_df])
    datedim_df=transform_to_datedim(all_date_df)
    return datedim_df

def create_Reviewdim(order_reviews_df):
    return order_reviews_df.drop("review_id")
 
def create_OrderFact(orders_df,order_items_df,Productdim_df,sellers_df,order_payments_df,PaymentTypedim_df):
    #customer_id already present in orders_df So no need to join the table
    joined_tables_df=orders_df.join(order_items_df,on="order_id",how="left")\
                          .join(order_payments_df,on="order_id",how="left")\
                          .join(Productdim_df,on="product_id",how="left")\
                          .join(sellers_df,on="seller_id",how="left")\
                          .join(PaymentTypedim_df,on="payment_type",how="left")
    orders_fact_df=joined_tables_df.select(["order_id","customer_id","seller_id","product_id",
                                            "price","freight_value","quantity","payment_sequential",
                                            "payment_installments","payment_value","payment_type_id"])
    return orders_fact_df

def create_OrderDateFact(orders_df):
    order_date_fact_df=orders_df.select('order_id',
                                   pl.col('order_purchase_timestamp').dt.to_string("%Y%m%d").cast(pl.Int64).alias("order_purchase_timestamp_key"), 
                                   pl.col('order_approved_at').dt.to_string("%Y%m%d").cast(pl.Int64).alias("order_approved_at_key"), 
                                   pl.col('order_delivered_carrier_date').dt.to_string("%Y%m%d").cast(pl.Int64).alias("order_delivered_carrier_date_key"),
                                   pl.col('order_delivered_customer_date').dt.to_string("%Y%m%d").cast(pl.Int64).alias("order_delivered_customer_date_key"), 
                                   pl.col('order_estimated_delivery_date').dt.to_string("%Y%m%d").cast(pl.Int64).alias("order_estimated_delivery_date_key"))
    return order_date_fact_df





    