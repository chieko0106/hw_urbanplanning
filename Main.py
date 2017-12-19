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

data4hierarchy = -1
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
print('linkage finished')
#将层级聚类结果以树状图表示出来并保存为plot_dendrogram.png
P=sch.dendrogram(Z)
plt.savefig('plot_dendrogram.png')
#根据linkage matrix Z得到聚类结果:
cluster = sch.fcluster(Z, t=0.1,criterion='distance')
print('cluster finished')
print("Original cluster by hierarchy clustering:{}".format(cluster))

#2. k-means聚类
#将原始数据做归一化处理
data=whiten(Points)
print('data whiten finished')
#使用kmeans函数进行聚类,输入第一维为数据,第二维为聚类个数k.
#有些时候我们可能不知道最终究竟聚成多少类,一个办法是用层次聚类的结果进行初始化.当然也可以直接输入某个数值.
#k-means最后输出的结果其实是两维的,第一维是聚类中心,第二维是损失distortion
centroid=kmeans(data,max(cluster))
print('k-means finished')

#使用vq函数根据聚类中心对所有数据进行分类,vq的输出也是两维的,[0]表示的是所有数据的label
label=vq(data,centroid[0])
k_means_label = label[0]

print ('Final clustering by k-means:{}'.format(k_means_label))

n = 0
for line in Interested_data:
    if n+1 == len(k_means_label):
        n = -1
    line['attributes']['Cluster'] = int(k_means_label[n])
    for kept_key in All_keys0[0:14]:
        line['attributes'][kept_key] = alldata['features'][n]['attributes'][kept_key]
    n = n+1
print('label append to alldata finished')
fp = open('Out.json','w')
json.dump(Interested_data,fp)
fp.close()

print('none')