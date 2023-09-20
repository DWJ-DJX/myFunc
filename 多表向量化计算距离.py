#encoding=utf-8


import pandas as pd
import numpy as np
import math
import timeit,time
import datetime
import re

path=r'C:\Users\DWJ\Desktop\5G路测\tmp\dt.csv'


# with open(path)as f:
#     for df in pd.read_csv(f,chunksize=2000,usecols=['路测ECI','NR Serving SS-RSRP_北区log2']):
#
#         df['NR Serving SS-RSRP_北区log2']=pd.to_numeric(df['NR Serving SS-RSRP_北区log2'],errors='coerce')
#
#         #pd.DataFrame().describe(include=[0])
#         #print(df.describe(include='O'))
#         group=df[['路测ECI','NR Serving SS-RSRP_北区log2']].groupby(by=['路测ECI'],as_index=False).agg({'NR Serving SS-RSRP_北区log2':['count','mean']})
#         print(group.columns.levels[0][[group.columns.labels[0]]])
#         print(group)
#         print("-"*30)


# df=pd.DataFrame(data=np.arange(40).reshape(10,4),index=[list("AABBCCDDEE"),list("1212121212")],columns=[["AA","AA","BB","BB"],["A1","A2","B1","B2"]])

#df=pd.DataFrame(data=np.concatenate((np.random.randint(1,20,20),np.random.randint(1,20,20)),axis=0).reshape(-1,4),index=list("ABCDEFGHIJ"),columns=["A1","A2","B1","B2"])
# path2=r'C:\Users\DWJ\Desktop\tmp.csv'
# with open(path2) as f:
#     df=pd.read_csv(f)
#
#
# df['aa']=df['RSRP'].rolling(window=3,min_periods=3,center=True).mean()#固定窗口长度
#
# df['bb']=df['RSRP'].expanding(min_periods=3,center=True).mean()#累计窗口长度，不固定



path12=r'C:\Users\DWJ\Documents\WeChat Files\q598110711\FileStorage\File\2019-12\鼎立平台指标模板-第十二轮2019-12-13(1).xlsx'
path11=r'C:\Users\DWJ\Documents\WeChat Files\q598110711\FileStorage\File\2019-12\基础优化测试指标-汇总20191031(2)(1).xlsx'





df12_4G=pd.read_excel(path12,sheet_name='3G',index_col='区域')
df11_4G=pd.read_excel(path11,sheet_name='19.8第十轮3G正向',index_col='区域')


cols=[]
for col in df12_4G.columns:
    if np.issubdtype(df12_4G[col],np.number):
        cols.append(col)
df12_4G=df12_4G[cols]

cols=[]
for col in df11_4G.columns:
    if np.issubdtype(df11_4G[col],np.number):
        cols.append(col)
df11_4G=df11_4G[cols]


xx=df12_4G-df11_4G


xx.to_csv(r'C:\Users\DWJ\Desktop\对比3G.csv',encoding='gbk')







