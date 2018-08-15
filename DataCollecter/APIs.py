from jaqs.data import DataApi
from sqlalchemy import create_engine
import tushare as ts

def getDBConn():
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
        # conn = engine.connect()
        return engine#, conn
    except Exception as e:
        print('----Can''t create connection to : ' + conn_str)

def getQuantApi():
    token = 'eyJhbGciOiJIUzI1NiJ9.eyJjcmVhdGVfdGltZSI6IjE1MzI5MzM3MjAwOTEiLCJpc3MiOiJhdXRoMCIsImlkIjoiMTg2MDExMTA5NTkifQ.nN08iv14dxEtd1r3EMmASxfkWqXoJ0xlyif8peWaFg4'
    addr = 'tcp://data.quantos.org:8910'
    phone = '18601110959'
    try:
        api = DataApi(addr = addr)
        api.login(phone, token)
        return api
    except Exception as e:
        print('Init Api Failed')

def getTushareApi():
    token = '67f84aad6e6089ae9669ea7c01b732de51f856568b559219f11f029e'
    try:
        ts.set_token(token) 
        tsapi = ts.pro_api()
        return tsapi
    except Exception as e:
        print('Init Api Failed')