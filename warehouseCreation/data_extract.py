from sqlalchemy import inspect
import polars as pl

class extraction():
    def __init__(self,sqlalchemy_conn):
        self.conn=sqlalchemy_conn
    
    def get_all_tables_name(self):
        inspect(self.conn).get_table_names()

    def get_all_tables_data(self):
        table_names=self.get_all_tables_name()
        query="select * from {}"
        return [(table_name, pl.read_database(query.format(table_name),self.conn)) for table_name in table_names]

    def get_tables_data(self,table_name_list):
        query="select * from {}"
        return [(table_name, pl.read_database(query.format(table_name),self.conn)) for table_name in table_name_list]

    def get_table_dataframe(self,table_name:str):
        query="select * from {}"
        return pl.read_database(query.format(table_name),self.conn)
    
    def query_to_dataframe(self,query:str):
        return pl.read_database(query),self.conn
