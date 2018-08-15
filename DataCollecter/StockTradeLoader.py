import APIs
import DataCollecterLog as dlog
import sys
import time
import tushare as ts

# Using quantOS which has only latest 5 years data
# deprecated function
def saveDailyTrade_quantos(_symbols, _start_dte, _end_dte):
    try:
        api = APIs.getQuantApi()
        # engine = APIs.getDBConn()
        df, msg = api.daily(
                    symbol= _symbols,
                    start_date=_start_dte,
                    end_date=_end_dte, 
                    fields="", 
                    adjust_mode=None)
        print(df)
        
        # df.to_sql('AStocks_Trade_Daily', engine, if_exists='append')
    except Exception as e:
        print('----failed at {}'.format(sys._getframe().f_code.co_name))
        print('--------',e,'--------')
    finally:
        # engine.dispose()
        pass

# 前复权数据
def saveHistoricalDailyTrade_qfq(_symbols, _start_dte, _end_dte):
    try:
        print('----Start processing historical data')
        # get DB connection 
        engine = APIs.getDBConn()

        # config parameters
        # _ktype = 'D' # D=日k线 W=周 M=月 5=5分钟 15=15分钟 30=30分钟 60=60分钟'
        _autype = 'qfq' # qfq-前复权 hfq-后复权 None-不复权，默认为qfq
        _index = False # 设定为True时认为code为指数代码
        # start = _start_dte # YYYY-MM-DD 为空时取当前日期
        # end = _end_dte # YYYY-MM-DD 为空时取当前日期

        df = ts.get_h_data(code=_symbols, start=_start_dte, end=_end_dte, autype=_autype, index=_index, retry_count = 3, pause = 0.5)
        df['symbol'] = _symbols
        df.to_sql('AStocks_Trade_Daily_qfq', con = engine, if_exists = 'append')
        # print(df)
        print('----Finish processing historical data')
    except Exception as e:
        print('----Failed at {}'.format(sys._getframe().f_code.co_name))
        dlog.writeLog(time.strftime('%Y%m%d %H:%M:%S', time.localtime()), sys._getframe().f_code.co_name, 'symbol = {}, start = {}, end = {}'.format(_symbols,_start_dte,_end_dte,), e )
    finally:
        engine.dispose()

saveHistoricalDailyTrade_qfq('000651','2018-01-01','2018-12-31')

# saveDailyTrade_quantos('sh',20120101,20120110)