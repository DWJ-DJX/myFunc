#encoding=utf-8


import numpy as np
import pandas as pd
import os
import shapely
from geopandas import GeoDataFrame,sjoin


r=6371393.0

def dist_(row,lng_a, lat_a, lng_b, lat_b):
    #供dataframe的apply使用，此处循环为迭代row
    cos_n= np.cos(90 - row[lat_a]) * np.cos(90 - row[lat_b]) + np.sin(90 - row[lat_a]) * np.sin(90 - row[lat_b]) * np.cos(row[lng_a] - row[lng_b])
    return np.radians(np.arccos(cos_n))*6371393.0

def lng_lat_b(df,lng_a, lat_a,AZ,dist):#az角度单位方位角，dist距离，返回B点经纬度
    n=df[dist]/r#∠n的弧度值
    b=np.radians(90-df[lat_a])#∠b的弧度值
    AZ=np.radians(df[AZ])#方位角的弧度值
    a=np.arccos(np.cos(b)*np.cos(n)+np.sin(b)*np.sin(n)*np.cos(AZ))
    N=np.arcsin(np.sin(AZ)*np.sin(n)/np.sin(a))
    df['lng_b']=np.degrees(N)+df[lng_a].values
    df['lat_b']=90-np.degrees(a)


def dist_azimuth(df,lng_a, lat_a, lng_b, lat_b):#返回距离及方位角
    a=np.radians(90 - df[lat_b])
    b=np.radians(90 - df[lat_a])
    N=np.radians(df[lng_b] - df[lng_a])
    cos_n= np.cos(a)*np.cos(b) + np.sin(a)*np.sin(b)*np.cos(N)
    dist=np.arccos(cos_n)*6371393.0
    sin_A = np.sin(a) * np.sin(N)/np.sqrt(1-cos_n**2)
    azimuth=np.degrees(np.arcsin(sin_A))
    azimuth=np.where(df[lat_b]<df[lat_a],180.0 - azimuth,azimuth)
    azimuth = np.where((df[lng_b] < df[lng_a]) & (df[lat_b] >= df[lat_a]), 360.0 + azimuth, azimuth)
    df['距离']=dist.values
    df['方位角']=azimuth

def lng_lat_x(df, id, lng, lat, AZ, dist, x):#id唯一标识,AZ角度单位方位角，dist距离，x扇形边缘点数
    df['顺序']=0
    if x==1:
        l=[df[AZ]]
    else:
        l=[]
        for i in range(x+1):
            l.append(df[AZ]-32.5+i*65/x)
    for i,az in enumerate(l):
        n=df[dist]/r#∠n的弧度值
        b=np.radians(90 - df[lat])#∠b的弧度值
        AZ=np.radians(az)#方位角的弧度值
        a=np.arccos(np.cos(b)*np.cos(n)+np.sin(b)*np.sin(n)*np.cos(AZ))
        N=np.arcsin(np.sin(AZ)*np.sin(n)/np.sin(a))
        df['顺序_'+str(i+1)]=i+1
        df['lng_'+str(i+1)]=np.degrees(N)+df[lng].values
        df['lat_'+str(i+1)]=90-np.degrees(a)
    df_all=df[[id,'顺序', lng, lat]]
    for j in range(1,i+2):
        _df=df[[id,'顺序_'+str(j),'lng_'+str(j),'lat_'+str(j)]].rename(columns={'顺序_'+str(j):'顺序','lng_'+str(j):lng, 'lat_' + str(j):lat})
        df_all=df_all.append(_df)
    df_all.sort_values(by=[id,'顺序'],ascending=True,inplace=True)
    return df_all

def read_csv(path_fold,encoding='gbk',usecols=None):
    df_all=pd.DataFrame()
    for file in os.listdir(path_fold):
        file = file.strip('~$')
        if not file.endswith('.csv'):
            continue
        # if not re.match("(?:东区单元([489]|10)|南区单元[3-8]|西区单元5).csv",file):
        #     continue
        with open(os.path.join(path_fold,file),encoding=encoding) as f:
            df=pd.read_csv(f,usecols=usecols)
        df_all=df_all.append(df)
    return df_all

def Point_Within_Polygon(df_point,csv_or_shp,buffer=500,lng_a=None,lat_a=None,lng_b=None,lat_b=None):
    #csv_or_shp传入的底图为csv或shp格式或geodataframe对象
    if csv_or_shp.endswith('.csv'):
        with open(csv_or_shp)as f:
            df_region=pd.read_csv(f)
        #df_region['geometry']=df_region.apply(lambda x:shapely.geometry.Point(x.lng_b,x.lat_b),axis=1)
        #df_region=GeoDataFrame(df_region,crs={'init':'egsg:4326'})
        geom = [shapely.geometry.Point(a,b) for a,b in zip(df_region[lng_b],df_region[lat_b])]
        df_region=GeoDataFrame(df_region, geometry=geom, crs='+init=epsg:4326')#初始为地理坐标系
        df_region.to_crs(crs={'init': 'epsg:32651'}, inplace='True')#转化为投影坐标系
        df_region['geometry']=df_region['geometry'].buffer(distance=buffer)
    elif csv_or_shp.endswith('.shp'):
        df_region=GeoDataFrame.from_file(csv_or_shp,encoding='gbk')
    else:
        df_region=csv_or_shp
    geom = [shapely.geometry.Point(a,b) for a,b in zip(df_point[lng_a],df_point[lat_a])]
    df_point=GeoDataFrame(df_point, geometry=geom, crs='+init=epsg:4326')#初始为地理坐标系
    df_point.to_crs(df_region.crs,inplace=True)
    df=sjoin(df_point,df_region, how='inner', op='within')
    del df['geometry']
    return df

def Sg(df,lng,lat,x=20,y=20):#地球半径=6371393.0
    x=np.degrees(x/5456740.9)#换算成经度差异
    y=np.degrees(y/6366197.7)# 换算成纬度差异
    df['lng1']=np.divmod(df[lng],x)[0]*x
    df['lat1'] = np.divmod(df[lat], x)[0]*x
    return df

def prename_(path, prefix: str, in_suffix=None, rollback=False):
    """
    :param path: 文件夹路径
    :param prefix: 需要添加的前缀
    :param in_suffix: 仅针对过滤的后缀名文件进行重命名
    :param rollback: True表示删除前缀，False表示增加前缀
    :return: 原地修改，重命名文件名
    """
    import os
    from collections import Iterable

    for root, folder, files in os.walk(path):
        for file in files:
            if rollback:  # 减前缀
                if not file.startswith(prefix):
                    continue
                if in_suffix:
                    if not ((isinstance(in_suffix, str) and in_suffix == file.rsplit('.', maxsplit=1)[1]) \
                            or (isinstance(in_suffix, Iterable) and file.rsplit('.', maxsplit=1)[1] in in_suffix)):
                        continue
                new_file = file.lstrip(prefix)
                os.rename(os.path.join(root, file), os.path.join(root, new_file))
            else:  # 加前缀
                if file.startswith(prefix):
                    continue
                if in_suffix:
                    if not ((isinstance(in_suffix, str) and in_suffix == file.rsplit('.', maxsplit=1)[1]) \
                            or (isinstance(in_suffix, Iterable) and file.rsplit('.', maxsplit=1)[1] in in_suffix)):
                        continue
                new_file = prefix + file
                os.rename(os.path.join(root, file), os.path.join(root, new_file))
# prename_(r'C:\Users\dwj\Desktop\aa',prefix='13轮#',in_suffix=['txt','csv'],rollback=True)
# 加前缀（不会重复加相同前缀），上例仅对txt,csv,docx文件生效


def pjjwd(df,col):#就算经纬度平均值(非中心经纬度)
    df['经度']=df[col].str.findall('(12[012].\d+),').apply(lambda x: np.mean(list(map(float,x))))
    df['纬度']=df[col].str.findall(',(3[01].\d+)').apply(lambda x: np.mean(list(map(float,x))))
    return df


def zxjwd(df,col):#中心经纬度
    df['lng'] = df[col].str.findall('(12[012].\d+),').apply(lambda x: list(map(float, x)))#提取经度
    df['lat'] = df[col].str.findall(',(3[01].\d+)').apply(lambda x: list(map(float, x)))#提取纬度
    df['lng_lat']=df.apply(lambda x:[a for a in zip(x['lng'],x['lat'])],axis=1)#将经纬度转换成易于处理的类WKT形式
    geom =df.apply(lambda x:shapely.geometry.Polygon(x['lng_lat']),axis=1)#构造geom
    df_region = GeoDataFrame(df.iloc[:,:-3], geometry=geom, crs='+init=epsg:4326')  #构造gdf
    df_region['zxjwd']=df_region.centroid#加中心经纬度
    return df_region


def _time(fun):
    import datetime
    x=datetime.datetime.now()

    def wrapper(*args,**kw):
        result=fun(*args,**kw)
        y = datetime.datetime.now()
        diff = (y - x).total_seconds()
        h, _ = diff // 3600, diff % 3600
        m, s = _ // 60, _ % 60
        print("耗时{:.0f}小时{:.0f}分钟{:.2f}秒".format(h, m, s))
        return result
    return wrapper

def make_date(start:str,):
    #按月递增string格式日期
    l =[]



