from models import geolocation,customers,order_items,order_payments,orders,products,sellers,order_reviews
from models import Base
from sqlalchemy.orm import sessionmaker,scoped_session
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import concurrent
import csv
import logging
Log_Format = "%(levelname)s %(asctime)s - %(message)s"

logging.basicConfig(filename = "logfile.log",
                    filemode = "w",
                    format = Log_Format, 
                    level = logging.ERROR)
logger = logging.getLogger()

#create engine for sql server to connect
connection_string = r"Driver={ODBC Driver 17 for SQL Server};Server=tcp:192.168.0.103,1433;Database=olist;Uid=prasad;Pwd=Suraj123;TrustServerCertificate=yes;Connection Timeout=30;"
connection_url=URL.create("mssql+pyodbc",query={"odbc_connect": connection_string})
engine=create_engine(connection_url)

def upload_data(session,table,data_path):
    data_path=data_path.format(table.__tablename__)
    try:
        with open(data_path,'r',encoding="utf-8") as inputfile:
            reader=list(csv.DictReader(inputfile))
            print("file is readed for path {}".format(data_path))
            print("bulk insert for table {} started".format(table.__tablename__))
            session.bulk_insert_mappings(table,reader)
            session.commit()
            print("bulk insert for table {} ended".format(table.__tablename__))
    except Exception as err:
        logger.error(err)
    finally:
        session.close()
    
list_of_class=[customers,sellers,products,orders,geolocation,order_payments,order_items,order_reviews]

def main():
    print("Creating table...")
    #Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("All Tables created....")
    session=scoped_session(sessionmaker(engine))
    data_path = "S:\\dataRepo\\olistdataset\\olist_{}_dataset.csv"
    print("data uploading is started......")
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        {executor.submit(upload_data, session, table, data_path): table for table in list_of_class}
    print("data uploading stoped....")

if __name__ == "__main__":
    main()
