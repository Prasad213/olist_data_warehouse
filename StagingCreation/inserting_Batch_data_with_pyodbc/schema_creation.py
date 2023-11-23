import pyodbc
import Schema
import Insert
import pandas as pd
from contextlib import contextmanager
import asyncio
import concurrent.futures

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
        cnxn = pyodbc.connect(connection_string, autocommit=True)
        #print("SQL Server connection is successful")
        yield cnxn
    except Exception as err:
        logger.error(err)
        #print(f"Error: '{err}'")
    finally:
        cnxn.close()

def create_schema(crsr, table_list, schema_dict):
    try:
        for table in table_list:
            crsr.execute(schema_dict[table])
        print("Schema is created")
    except Exception as err:
        #logger.error(err)
        print(f"Error: '{err}'")

def modify_data(row):
    listed_data=(tuple(row))
    #('4aba391bc3b88717ce08eb11e44937b2', 45816, "arraial d'ajuda (porto seguro)", 'BA') convert this for insert query
    modified_data=tuple(map(lambda x: x.replace("'","") if(type(x)==str) else x,listed_data))
    return str(modified_data).replace(', nan',', Null')

def upload_data(connection_string, table_name, insert_dict, data_path):
    path = data_path.format(table_name)
    dataframe = pd.read_csv(path)
    count = 0
    query = insert_dict[table_name]
    final_query=query
    print("upload start for ",table_name)

    with get_connection(connection_string) as connection:
        crsr=connection.cursor()
        for row in dataframe.itertuples(index=False):
            if(count < 999):
                final_query += modify_data(row)+","
                count += 1
            else:
                crsr.execute(final_query.rstrip(",")+";")                                           #print(final_query.rstrip(",")+";")                  
                count=0
                final_query=query
                final_query += modify_data(row)+","          #while else runs on of row is there
        #after ending for loop remainng final_query will execute
        crsr.execute(final_query.rstrip(",")+";")
    print("upload end for",table_name)

def main():
    schema_dict = Schema.__dict__
    table_list = [table for table in schema_dict if table.startswith("olist")]
    insert_dict = Insert.__dict__
    connection_string = r"Driver={SQL Server};Server=tcp:pract-data-server.database.windows.net,1433;Database=olist;Uid=practiceuser;Pwd=DhjTo8fq2Cbvge;TrustServerCertificate=yes;Connection Timeout=30;"
    # with get_connection(connection_string) as cnxn:
    #     crsr = cnxn.cursor()
    #     create_schema(crsr, table_list, schema_dict)
    data_path = "S:\\dataRepo\\olistdataset\\{}.csv"
    print("data uploading is started......")
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        result_set = {executor.submit(upload_data, connection_string, table_name,insert_dict, data_path): table_name for table_name in table_list}
        # end_res = result_set.keys()
    print("data uploading stoped....")


if __name__ == "__main__":
    main()
