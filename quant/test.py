import matplotlib.pyplot as plt
import matplotlib.finance as mpf
import pandas as pd
import numpy as np
from matplotlib.pylab import date2num
import datetime

raw = [
    ['20180101',1.1,2.1,0.9,1.6],
    ['20180103',2.0,3.0,0.9,1.4],
    ['20180104',1.1,2.1,0.9,1.6],
    ['20180105',2.0,3.0,0.9,5.0],
    ['20180108',1.1,2.1,0.9,0.5],
    ['20180109',2.0,3.0,0.9,2.5],
    ['20180110',1.1,2.1,0.9,1.1],
]

df = pd.DataFrame(raw,columns=['t','open','high','low','close'])
# print(df)
data = []
item = []
dt = []
for i in df.iterrows():
    item = [i[0],i[1]['open'],i[1]['high'],i[1]['low'],i[1]['close']]
    data.append(item)
    dt.append(i[1]['t'])
dt.insert(0,1)
# v = np.array(data)

# for i in range(len(raw)):
#     # t = date2num(datetime.datetime.strptime(raw[i][0],'%Y%m%d'))
      # o, h, l ,c = raw[i][1:5]
#     data = (i, o, h, l, c)
#     # print(raw[i][0])
#     dt.append(raw[i][0])
#     v.append(data)
# # print(v)
# # print(dt)
# dt.insert(0,'0')
# print(dt)
fig, ax = plt.subplots(facecolor=(0.5, 0.5, 0.5))
fig.subplots_adjust(bottom=0.2)
# ax.xaxis_date()
plt.title('K Line Test')
plt.xlabel('Days')
plt.ylabel('Price')
# plt.grid()
# ax.set_xticks(dt)
ax.set_xticklabels(dt, rotation=45, ha='right')

mpf.candlestick_ohlc(ax, data, width=0.3, colorup='r', colordown='green', alpha=1.0)
plt.show()
