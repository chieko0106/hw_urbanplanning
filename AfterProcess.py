# -*- coding:utf-8 -*-
import json
with open('Out.json','r') as f:
    newdata=json.load(f)
    f.close()
path="Streets_Harvey_FeaturesToJSO.json"
with open(path,'r') as f:
    olddata=json.load(f)
    f.close()

dic_RoadID2Chara = {}
for line in newdata:
    line = line['attributes']
    Road_ID = str(line['ROAD_ID'])
    if Road_ID not in dic_RoadID2Chara.keys():
        dic_RoadID2Chara[Road_ID] = {'Nature':[],'City':[],'Flow':[],'Passage':[],'Noise':[],'Cluster':[]}
    for key,value in line.items():
        if key in dic_RoadID2Chara[Road_ID].keys():
            dic_RoadID2Chara[Road_ID][key].append(value)
keys = []
for key,value in dic_RoadID2Chara['80'].items():
    if key !='Cluster':
        keys.append(key)
for line in dic_RoadID2Chara:
    for key in keys:
        value = dic_RoadID2Chara[line][key]
        key_diff = key+'_diff'
        Average = sum(value)/len(value)
        Diff = (max(value)-min(value))/len(value)
        dic_RoadID2Chara[line][key] = Average
        dic_RoadID2Chara[line][key_diff] = Diff
'''
重新聚类
'''
#根据街道均值重新聚类
import numpy as np
import scipy.cluster.hierarchy as sch
from scipy.cluster.vq import vq,kmeans,whiten
import matplotlib.pylab as plt

Points = []
for line in dic_RoadID2Chara:
    element = []
    for key in keys:
        key_diff = key + '_diff'
        element.append(dic_RoadID2Chara[line][key])
        element.append(dic_RoadID2Chara[line][key_diff])
    Points.append(np.array(element))
Points = np.array(Points)

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
cluster = sch.fcluster(Z, t=0.2,criterion='distance')
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
for key,value in dic_RoadID2Chara.items():
    dic_RoadID2Chara[key]['Cluster'] = int(k_means_label[n]) #注意这里int了一下，主要是为了json输出的时候可以序列化
    n = n+1

Road_IDs = []
for key,value in dic_RoadID2Chara.items():
    Road_IDs.append(key)

A = ['Green_Matlab','SD_Green','Pano_per_k','WIDTH_infer','HEIGHT1','HEIGHT2']
B = ['Cluster','Nature','City','Flow','Passage','Noise']
for line in olddata['features']:
    line = line['attributes']
    key = str(line['ROAD_ID'])
    if key in Road_IDs:
        for i in range(len(A)):
            line[A[i]] = dic_RoadID2Chara[key][B[i]]
    else:
        line['Green_Matlab'] = -1
        line['SD_Green'] = 0
        line['Pano_per_k'] = 0
        line['WIDTH_infer'] = 0
        line['HEIGHT1'] = 0
        line['HEIGHT2'] = 0

for i in range(len(A)):
    olddata['fieldAliases'][A[i]] = B[i]
for line in olddata['fields']:
    if line['name'] in A:
        line['alias'] = B[A.index(line['name'])]

fp = open('St_View_Line_Kmeans.json','w')
json.dump(olddata,fp)
fp.close()
print('after processing finished')