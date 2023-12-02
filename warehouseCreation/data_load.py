from sqlalchemy import Connection
import polars as pl


def insert_data(table_name:str,datframe:pl.DataFrame,conn:Connection):
    try:
        pd_df=datframe.to_pandas()
        
        pd_df.to_sql(name=table_name,con=conn,if_exists='append',index=False) #if table not exist it create or append data to it
    except Exception as err:
        print(f"{table_name} :::: {err}")
       