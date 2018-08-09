import time
import sys
import re
import requests
import json
import pandas as pd
import numpy as np
import pymysql
from sqlalchemy import create_engine 
from pprint import pprint
from bs4 import BeautifulSoup

# news of which date you want to collect
# generate a timestamp in python and pass this parameter in request
startDate = '2018-07-29 12:00:00'
endDate = '2018-01-01 23:59:59'

startts = str(int(time.mktime(time.strptime(startDate,'%Y-%m-%d %H:%M:%S'))))
endts = 1532530758 #int(time.mktime(time.strptime(endDate,'%Y-%m-%d %H:%M:%S')))
# print(ts)

# Parameters
baseUrl = 'https://api-prod.wallstreetcn.com/apiv1/content/lives?channel=a-stock-channel&client=pc'
pTimestamp = startts
pLimit = '99'

# Global Variables
# finalResult = []
engine = ''
conn = ''
def intiParameter():
    # global finalResult
    global engine
    global conn
    engine, conn = getDB()

# User-Agent
def getUserAgent():
    head = {}
    head['User-Agent'] = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1' #random.choice(user_agents)
    head['Accept'] = 'application/json, text/plain, */* '
    head['Accept-Encoding'] = 'gzip, deflate, br'
    head['Connection'] = 'keep-alive'
    head['Cache-Control'] = 'no-cache'
    head['Accept-Language'] = 'zh-CN,zh;q=0.9,en;q=0.8'
    head['Cookie'] = '__ah_uuid=A2B15090-18FD-408C-A33B-8C176DB246CF; fvlid=1528449591077hFaJIcNCDP; sessionid=A9457D16-F1F9-417A-8A79-6139DD4E7B6F%7C%7C2018-06-08+17%3A19%3A49.956%7C%7Ccn.bing.com; ahpau=1; sessionuid=A9457D16-F1F9-417A-8A79-6139DD4E7B6F%7C%7C2018-06-08+17%3A19%3A49.956%7C%7Ccn.bing.com; historybbsName4=c-4473%7C%E8%8D%A3%E5%A8%81RX3%E8%AE%BA%E5%9D%9B%2Cc-110%7C%E5%87%AF%E7%BE%8E%E7%91%9E%E8%AE%BA%E5%9D%9B%2Cc-588%7C%E5%A5%94%E9%A9%B0C%E7%BA%A7%E8%AE%BA%E5%9D%9B; area=110199; __lnkrntdmcvrd=-1; __utma=1.1956891062.1528450821.1529205553.1529990390.5; __utmz=1.1529990390.5.3.utmcsr=autohome.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/beijing/; pcpopclub=8fd2b31debb94362b9adf0120d113235011f89b4; clubUserShow=18844084|66|2|Mr__Shawn|0|0|0||2018-06-26 13:20:40|0; autouserid=18844084; sessionuserid=18844084; sessionip=123.113.157.85; ahsids=588_56_110_4473; sessionvid=80D6409C-6392-498B-AD54-135F0A26486A; sessionlogin=0f2091e8ca364891a0ec58593a68102f011f89b4; autoac=EF880E3E000C263A533B8B1175334B54; autotc=E6213439FBB4EDB60885FE5F1D999638; ASP.NET_SessionId=cokhhgnoobypdarjf0bgnmoq; ahpvno=139; ref=127.0.0.1%7C0%7C0%7Ccn.bing.com%7C2018-06-27+23%3A00%3A05.043%7C2018-06-26+20%3A47%3A43.254; ahrlid=1530111601676vbcpBpZ38w-1530111605869'
    head['Pragma'] = 'no-cache'
    head['host'] = 'api-prod.wallstreetcn.com'
    head['origin'] = 'https://wallstreetcn.com'
    head['Referer'] = 'https://wallstreetcn.com/live/a-stock'
    head['X-Client-Type'] = 'pc'
    head['X-Device-Id'] = 'pcwscn-164ccb48-8577-6a1d-f174-594d17496367'
    head['X-Ivanka-Platform'] = 'wscn-platform'
    
    return head

def getDate(_ts):
    dt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(_ts)))
    return dt

def getNews(_cur, _limit = 2):
    try:
        reqList = []
        url = baseUrl + '&cursor={0}&limit={1}'.format(_cur,_limit)
        req = requests.get(url,headers=getUserAgent())
        time.sleep(5)
        print('---- Start geting data from {0}:'.format(url))
        rawnews = req.content.decode('utf8')
        # pprint(rawnews)
        nextCursor, reqList = extractData(rawnews)
        # finalResult.extend(reqList)
        persistData(reqList)
        if int(nextCursor) >= endts:
            getNews(_cur = nextCursor, _limit = 99)
        # print('Done')
    except Exception as e:
        print('---- Failed geting data from {0}:'.format(url))
        print(sys.exc_info())

def extractData(_data):
    # columns: artical_id, artical_content, artical_url, artical_time
    # raw = '{"code":20000,"message":"OK","data":{"items":[{"article":null,"channels":["a-stock-channel"],"content":"【长春市人民检察院依法介入“长生疫苗”事件】根据最高人民检察院部署，长春市人民检察院按照吉林省人民检察院要求，7月23日依法成立专案组，对“长生疫苗”事件开展调查。目前，专案组已提前介入公安机关侦查，引导调查取证，做好依法追究有关人员责任衔接；对“长生疫苗”损害公共利益情况及相关行政机关履职情况展开调查。检察机关将积极配合国务院调查组，依法做好相关工作。","content_more":"","content_text":"【长春市人民检察院依法介入“长生疫苗”事件】根据最高人民检察院部署，长春市人民检察院按照吉林省人民检察院要求，7月23日依法成立专案组，对“长生疫苗”事件开展调查。目前，专案组已提前介入公安机关侦查，引导调查取证，做好依法追究有关人员责任衔接；对“长生疫苗”损害公共利益情况及相关行政机关履职情况展开调查。检察机关将积极配合国务院调查组，依法做好相关工作。","display_time":1532443967,"global_channel_name":"7x24快讯","global_more_uri":"wscn://wallstreetcn.com/live","id":1311567,"image_uris":["https://baoimage.wallstreetcn.com/FsG_EDW6TLJb1p8e1Pr3CT8t_hxQ?watermark/3/image/aHR0cDovL2ltYWdlLmJhby53YWxsc3RyZWV0Y24uY29tL3dhdGVyX21hcmtfdjUucG5n/dissolve/100/gravity/Center"],"is_favourite":false,"is_priced":false,"reference":"","score":1,"symbols":[],"tags":[],"title":""},{"article":null,"channels":["a-stock-channel"],"content":"【证监会：迈瑞生物等四家公司首发获通过】证监会官网消息，深圳迈瑞生物医疗电子股份有限公司（首发）、无锡蠡湖增压技术股份有限公司（首发）、杭州迪普科技股份有限公司（首发）获通过、宁波兴瑞电子科技股份有限公司（首发）获通过。安徽金春无纺布股份有限公司（首发）未通过","content_more":"","content_text":"【证监会：迈瑞生物等四家公司首发获通过】证监会官网消息，深圳迈瑞生物医疗电子股份有限公司（首发）、无锡蠡湖增压技术股份有限公司（首发）、杭州迪普科技股份有限公司（首发）获通过、宁波兴瑞电子科技股份有限公司（首发）获通过。安徽金春无纺布股份有限公司（首发）未通过","display_time":1532442923,"global_channel_name":"7x24快讯","global_more_uri":"wscn://wallstreetcn.com/live","id":1311554,"image_uris":[],"is_favourite":false,"is_priced":false,"reference":"","score":1,"symbols":[],"tags":[],"title":""}],"next_cursor":"1532442923","polling_cursor":"1311567"}}'
    data = json.loads(_data)
    result = {}
    resultList = []
    tmp = {}
    # pprint(data)
    items = data['data']['items']
    nextCursor = data['data']['next_cursor']
    for item in items:
        result['artical_id'] = item['id']
        result['artical_content'] = item['content_text']
        result['artical_ts'] = item['display_time']
        result['artical_time'] = getDate(item['display_time'])
        tmp = result.copy()
        resultList.append(tmp)
        result = {}
    # pprint(resultList)
    return nextCursor, resultList

def persistData(_data):
    try:
        # engine, conn = getDB()
        df = pd.DataFrame(_data, columns = ['artical_id','artical_content','artical_ts','artical_time'])
        # print(df)
        df.to_sql(name='AStock_News', con=conn, if_exists='append', index=False)
        print('persist data done')
    except Exception as e:
        print(e)

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

intiParameter()
getNews(_cur = startts,_limit=99)
conn.close()
engine.dispose()

# print(finalResult)
# persistData(finalResult)