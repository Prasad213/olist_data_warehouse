import pyodbc
import Schema 
import insertqueries
import pandas as pd 
from contextlib import contextmanager
import concurrent.futures
import numpy as np
import logging
Log_Format = "%(levelname)s %(asctime)s - %(message)s"

logging.basicConfig(filename = "logfile.log",
                    filemode = "w",
                    format = Log_Format, 
                    level = logging.ERROR)
logger = logging.getLogger()

@contextmanager
def get_connection(connection_string):
    try:
        cnxn = pyodbc.connect(connection_string,autocommit=True)
        print("SQL Server connection is successful")
        yield cnxn
    except Exception as err:
        logger.error(err)
        #print(f"Error: '{err}'")
    finally:
        cnxn.close()

def create_schema(crsr,table_list,schema_dict):
    try:
        for table in table_list:
            crsr.execute(schema_dict[table])
        print("Schema is created")
    except Exception as err:
        logger.error(err)
        #print(f"Error: '{err}'")

def upload_data(connection_string,table_name,insert_dict,data_path):
    try:
        path=data_path.format(table_name)
        dataframe=pd.read_csv(path)
        dataframe = dataframe.fillna(np.nan).replace([np.nan], [None]) #nan as null object is not recognised in pyodbc so we use None pythons null
        query=insert_dict[table_name]
        from datetime import datetime
        start_time = datetime.now()
        print("data insertion is satrted for ",table_name)
        with get_connection(connection_string) as cnxn:
            crsr = cnxn.cursor()
            crsr.fast_executemany=True
            crsr.executemany(query,dataframe.itertuples(index=False))
            crsr.commit()
            
            # for row in dataframe.itertuples(index=False):
            #     insert_data(crsr,query,row)
        end_time = datetime.now()
        print("data insertion is end for ",table_name," Duration: ", end_time - start_time)
        
    except Exception as err:
        logger.error(err)
        print(f"{table_name} :: Error: '{err}'")
        

def insert_data(crsr,query,row):
    try:
            crsr.execute(query,tuple(row))
    except Exception as err:
        #print(tuple(row),err)
        val=str(tuple(row))+"::"+str(err)
        logger.error(val)
        


def main():
    schema_dict=Schema.__dict__
    table_list=[table for table in schema_dict if table.startswith("olist") ]
    insert_dict=insertqueries.__dict__
    connection_string=r"Driver={ODBC Driver 17 for SQL Server};Server=tcp:192.168.0.103,1433;Database=olist;Uid=prasad;Pwd=Suraj123;TrustServerCertificate=yes;Connection Timeout=30;"
    # with get_connection(connection_string) as cnxn:
    #     crsr = cnxn.cursor()
    #     create_schema(crsr,table_list,schema_dict)
    data_path="S:\\dataRepo\\olistdataset\\{}.csv"
    print("data uploading is started......")
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        {executor.submit(upload_data,connection_string,table_name,insert_dict,data_path): table_name for table_name in table_list}
        
    print("data uploading stoped....")
 
if __name__ == "__main__":
    main()

