import numpy as np
import pandas as pd
import os,re
import shapely,shapely.geometry
import geopandas as gpd
from geopandas import GeoDataFrame,sjoin
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt



# polygon1 = gpd.GeoDataFrame({
#     'value1': [1, 2,3],
#     'value2':['亚洲','非洲','亚洲'],
#     'geometry': [shapely.geometry.Polygon([(-1, -1), (1, -1), (2.5,2.5), (-1,1)]),
#                  shapely.geometry.Polygon([(1.5, 1.5), (2.5, 1.5), (2.5, 2.5), (1.5, 2.5)]),
#                  shapely.geometry.Polygon([(3, 3), (4, 3), (4, 4), (3, 4)])]
# }).unary_union
# print(polygon1)
#
# # point2 = gpd.GeoDataFrame({'geometry':[shapely.geometry.Point(0, 0), shapely.geometry.Point(2, 2)]})
# #
# # sjoin_result=gpd.sjoin(polygon1, point2, how='inner', op='contains')
# #inner内连接且最终结果来自左表，left左连接且最终结果来自左表，right...
# #intersects表示相交，within表示左表被包含，contains...
#
# # print(point2)
# # print(sjoin_result)
#
#
# ax = polygon1.plot(color='red', alpha=0.4)
# # ax = point2.plot(color='grey', alpha=0.4, ax=ax)
# # ax = sjoin_result.plot(color='black', alpha=0.4, ax=ax)
# # ax2=sjoin_result.plot(color='green', alpha=0.6)
# # plt.savefig('图14.png', dpi=300, bbox_inches='tight', pad_inches=0)


# path1=r'C:\Users\dwj\Desktop\temp\全量居民区0201.shp'
# path2=r'C:\Users\dwj\Desktop\居民区\上海居民区图层-增补\全量居民区0603.shp'
#
# # gdf1=GeoDataFrame.from_file(path1,encoding='gbk')
# gdf2=GeoDataFrame.from_file(path2,encoding='gbk')


# gdf1['area']=gdf1.area
# gdf1.to_csv(r'C:\Users\dwj\Desktop\temp\bbb.csv',encoding='gbk')

# gdf2.drop_duplicates(subset=['居民区名称'],keep='first',inplace=True)
# gdf2.to_file(r'C:\Users\dwj\Desktop\居民区\上海居民区图层-增补\全量居民区0603_.shp',encoding='gbk')
#
# x=gdf1['geometry'].centroid
# print(gdf1)




# gdf_inter=gpd.sjoin(gdf1,gdf2,how='inner',op='intersects').drop_duplicates(subset=['name'])['name'].values
#
# df_all=gdf1.append(gdf2.loc[~gdf2['name'].isin(gdf_inter)])
#
# df_all.update(df_all['name'].rename(index='居民区名称'),overwrite=False,)
# df_all[['居民区名称','geometry']].to_file(r'C:\Users\dwj\Desktop\temp\aaa.shp',encoding='gbk')


# gdf_inter=gpd.overlay(gdf1,gdf2)


# array = [1, 8, 15]
# g = (x for x in array if array.count(x) > 0)
# array = [2, 8, 22]
# print(list(g))#[8]
#
# array_1 = [1,2,3,4]
# g1 = (x for x in array_1)
# array_1 = [1,2,3,4,5]
# print(list(g1))
#
# array_2 = [1,2,3,4]
# g2 = (x for x in array_2)
# array_2[:] = [1,2,3,4,5]
#
#
# print(list(g2))


# funcs = []
# results = []
# for x in range(7):
#     def some_func():
#         return x
#     funcs.append(some_func)
#     results.append(some_func()) # 注意这里函数被执行了
#
# funcs_results = [func() for func in funcs]
#
# print(x)

