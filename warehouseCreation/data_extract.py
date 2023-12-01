from sqlalchemy import Connection
import polars as pl

def get_all_tables_name(sqlalchemy_conn:Connection):
    from sqlalchemy import inspect
    return inspect(sqlalchemy_conn).get_table_names()

def get_all_tables_data(sqlalchemy_conn:Connection):
    table_names=get_all_tables_name(sqlalchemy_conn)
    query="select * from {}"
    return [pl.read_database(query.format(table_name),sqlalchemy_conn) for table_name in table_names]
    
def get_table_dataframe(table_name:str,sqlalchemy_conn:Connection):
    query="select * from {}"
    return pl.read_database(query.format(table_name),sqlalchemy_conn)
    
def query_to_dataframe(query:str,sqlalchemy_conn:Connection):
    return pl.read_database(query,sqlalchemy_conn)