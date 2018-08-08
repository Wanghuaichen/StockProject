import tushare as ts
from sqlalchemy import create_engine

# Global Variables
# finalResult = []
engine = ''
conn = ''
def intiParameter():
    # global finalResult
    global engine
    global conn
    engine, conn = getDB()

def getDB():
    config = {
        'user': 'dw',
        'password': 'shangSXY8797',
        'host': '127.0.0.1',
        'database': 'stock',
        'raise_on_warnings': True,
    }   
    try:
        conn_str = 'mysql+pymysql://dw:shangSXY8797@localhost/stock?charset=utf8'
        engine = create_engine(conn_str) 
        conn = engine.connect()
        return engine, conn
    except Exception as e:
        print('----Can''t create connection to : ' + conn_str)

def getBaiscStocks():
    df = ts.get_stock_basics()
    # print(df)
    df.to_sql('AStocks', engine, if_exists='append')

intiParameter()
getBaiscStocks()
conn.close()
engine.dispose()
