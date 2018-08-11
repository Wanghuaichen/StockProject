import sys
import os
import time

def getLogFile():
    codeingDirectory = os.getcwd()
    projectPath = 'StockProject'
    dt = time.strftime('%Y%m%d', time.localtime())

    logFilename = 'StockingDataProcessingLog_' + dt
    logFileFullPath = codeingDirectory + '/' + projectPath + '/' + logFilename + '.log'
    # print(logFileFullPath)

    try:
        logFile = open(logFileFullPath, mode='a')
        return logFile
    except Exception as e:
        print('----Failed at {}'.format(sys._getframe().f_code.co_name))
        print('--------',e,'--------')

def writeLog(datestamp, function, parameters, detail):
    logfile = getLogFile()
    logfile.write('='*20 + '\n')
    logfile.write('datestamp:       {}'.format(datestamp) + '\n')
    logfile.write('function name:   {}'.format(function)+ '\n')
    logfile.write('parameters:      {}'.format(parameters)+ '\n')
    logfile.write('detail:          {}'.format(detail)+ '\n')
    logfile.write('='*20 + '\n')
    logfile.close()
