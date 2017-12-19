# -*- coding:utf-8 -*-
import json
import numpy
#载入Arcgis中导出的数据
path="StreetViewPictures_point_Seg.json"
with open(path,'r') as f:
    alldata=json.load(f)
    f.close()
data=alldata['features']
#使用key索引得到所有data，这里暂时没用，只是调试
from Tools import get_list_by_key
Tree = get_list_by_key(data,'Tree')

dataslice = data[0]['attributes']
All_keys0=[]
for key, value in dataslice.items():
    All_keys0.append(key)

#把原来数据中的数据整合成感兴趣的数据
from Tools import  Data2Interested
Interested_data = Data2Interested(data)

dataslice = Interested_data[0]['attributes']
All_keys=[]
for key, value in dataslice.items():
    All_keys.append(key)

data4hierarchy = 100
from Tools import Data4HC
Points = Data4HC(Interested_data[0:data4hierarchy],All_keys[0:-1])

print('Get data finished')

import scipy.cluster.hierarchy as sch
from scipy.cluster.vq import vq,kmeans,whiten
import numpy as np
import matplotlib.pylab as plt
#1. 层次聚类
#生成点与点之间的距离矩阵,这里用的欧氏距离:
disMat = sch.distance.pdist(Points,'euclidean')
print('disMat finished')
#进行层次聚类:
Z=sch.linkage(disMat,method='average')
#将层级聚类结果以树状图表示出来并保存为plot_dendrogram.png
P=sch.dendrogram(Z)
plt.savefig('plot_dendrogram.png')
#根据linkage matrix Z得到聚类结果:
cluster = sch.fcluster(Z, t=1,criterion='inconsistent')

print("Original cluster by hierarchy clustering:{}".format(cluster))

print('none')