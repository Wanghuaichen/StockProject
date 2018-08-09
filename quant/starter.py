from jaqs.data import DataApi
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
import pandas as pd
import numpy as np

# parameters
token = 'eyJhbGciOiJIUzI1NiJ9.eyJjcmVhdGVfdGltZSI6IjE1MzI5MzM3MjAwOTEiLCJpc3MiOiJhdXRoMCIsImlkIjoiMTg2MDExMTA5NTkifQ.nN08iv14dxEtd1r3EMmASxfkWqXoJ0xlyif8peWaFg4'
addr = 'tcp://data.quantos.org:8910'
phone = '18601110959'
api = ''

def initApi():
    try:
        global api
        api = DataApi(addr = addr)
        api.login(phone, token)
    except Exception as e:
        print('Init Api Failed')

# Basic information views
# 接口	            view	                分类
# 证券基础信息表    jz.instrumentInfo	    基础信息
# 交易日历表	   jz.secTradeCal	        基础信息
# 分配除权信息表	lb.secDividend	        股票
# 复权因子表	    lb.secAdjFactor	        股票
# 停复牌信息表	    lb.secSusp	            股票
# 行业分类表	    lb.secIndustry	        股票
# 行业代码表	    lb.industryType	        股票
# 指数基本信息表	lb.indexInfo	        指数
# 指数成份股表	    lb.indexCons	        指数
# 公募基金净值表	lb.mfNav	            基金

def getViews():
    df, msg = api.query(
        view = 'lb.industryType',
        fields='industry_src, level, industry_code, industry_name',
        filter='industry_src=中证指数有限公司&level=level1',
        data_format='pandas'
    )
    print(df)

# trade data
def getTrade():
    data = []
    item = []
    dt = []
    df, msg = api.daily(
                symbol="002766.SZ", 
                start_date=20180308,
                end_date=20180808, 
                fields="", 
                adjust_mode='post')
    for i in df.iterrows():
        item = [i[0],i[1]['open'],i[1]['high'],i[1]['low'],i[1]['close']]
        data.append(item)
        dt.append(i[1]['trade_date'])
    dt.insert(0,1)
    fig, ax = plt.subplots(facecolor=(0.5, 0.5, 0.5))
    fig.subplots_adjust(bottom=0.2)
    # ax.xaxis_date()
    plt.title("K Line")
    plt.xlabel("Date")
    plt.ylabel("Price")
    # plt.grid()
    ax.set_xticklabels(dt, rotation=45, ha='right')
    mpf.candlestick_ohlc(ax, data, width=0.6, colorup='r', colordown='g', alpha=1.0)
    plt.show()

initApi()
getTrade()