from sqlalchemy import inspect
import pandas as pd

class extractor():
    def __init__(self,sqlalchemy_conn):
        self.conn=sqlalchemy_conn
    
    def get_all_tables_name(self):
        inspect(self.conn).get_table_names()

    def get_all_tables_data(self):
        table_names=self.get_all_tables_name()
        [(table_name,pd.read_sql_table(table_name,self.conn)) for table_name in table_names]

    def get_tables_data(self,table_name_list):
        [(table_name,pd.read_sql_table(table_name,self.conn)) for table_name in table_name_list]

    def get_table_dataframe(self,table_name:str):
        pd.read_sql_table(table_name,self.conn)
    
    def query_to_dataframe(self,query:str):
        pd.read_sql_query(query,self.conn)
