import APIs
import sys

def saveDailyTrade(_symbols, _start_dte, _end_dte):
    try:
        api = APIs.getQuantApi()
        engine = APIs.getDBConn()
        df, msg = api.daily(
                    symbol= _symbols,
                    start_date=_start_dte,
                    end_date=_end_dte, 
                    fields="", 
                    adjust_mode=None)
        
        df.to_sql('AStocks_Trade_Daily', engine, if_exists='append')
    except Exception as e:
        print('----failed at {}'.format(sys._getframe().f_code.co_name))
        print('--------',e,'--------')
    finally:
        engine.dispose()

saveDailyTrade('000333.SZ',20080101,20080131)