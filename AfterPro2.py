# -*- coding:utf-8 -*-
'''
根据之前的聚类结果，对各个类进行打分
'''
import json
with open('St_View_Line_Kmeans.json','r') as f:
    data=json.load(f)
    f.close()

dic_ClusterChara = {}
newdata = data['features']

def B2A(b):
    A = ['Green_Matlab', 'SD_Green', 'Pano_per_k', 'WIDTH_infer', 'HEIGHT1', 'HEIGHT2']
    B = ['Cluster', 'Nature', 'City', 'Flow', 'Passage', 'Noise']
    if b in B:
        a = A[B.index(b)]
    else:
        a = 'Input_b_NotIn_B'
    return a
def A2B(a):
    A = ['Green_Matlab', 'SD_Green', 'Pano_per_k', 'WIDTH_infer', 'HEIGHT1', 'HEIGHT2']
    B = ['Cluster', 'Nature', 'City', 'Flow', 'Passage', 'Noise']
    if a in A:
        b = B[A.index(a)]
    else:
        b = 'Input_a_NotIn_A'
    return b

for line in newdata:
    line = line['attributes']
    Cluster_ID = str(line[B2A('Cluster')])
    if Cluster_ID not in dic_ClusterChara.keys():
        dic_ClusterChara[Cluster_ID] = {'Nature':[],'City':[],'Flow':[],'Passage':[],'Noise':[]}
    for key,value in line.items():
        if A2B(key) in dic_ClusterChara[Cluster_ID].keys():
            dic_ClusterChara[Cluster_ID][A2B(key)].append(value)

keys = []
for key,value in dic_ClusterChara['0'].items():
    keys.append(key)
for line in dic_ClusterChara:
    for key in keys:
        value = dic_ClusterChara[line][key]
        Average = sum(value)/len(value)
        Diff = (max(value)-min(value))/len(value)
        dic_ClusterChara[line][key] = Average

def get_by_key(data,key):
    Out = []
    for line in data:
        line = data[line]
        Out.append(line[key])
    return Out

dic_Sort = {}
for key,value in dic_ClusterChara['0'].items():
    dic_Sort[key] = sorted(get_by_key(dic_ClusterChara,key))


'''
设置最优点比例
'''
Opted_Po = {'Nature':1.0,'City':0.3,'Flow':0.3,'Passage':0.6,'Noise':0.01}
keys = []
for key,value in dic_ClusterChara.items():
    keys.append(key)
'''
计算分数
'''
import numpy as np
from scipy.linalg import solve
for key in keys:
    line = dic_ClusterChara[key]
    line['TotalScore'] = 0
    for key in Opted_Po.keys():
        x = line[key]
        c_percent = Opted_Po[key]
        a0 = dic_Sort[key][1]
        b0 = dic_Sort[key][-1]
        Eps = (b0-a0)*0.01#对插值函数做一个小小的平移
        a = a0-Eps
        b = b0+Eps
        c = a0+(b0-a0)*c_percent
        ele_score = 10
        if x <= c:
            x1 = a
        else:
            x1 = b
        A_ = np.array([[x1**2-2*c*x1,1.0],[-c**2,1.0]])
        b = np.array([0.0,ele_score])
        c_ = solve(A_,b)
        line[key+'Score'] = (x**2-2*c*x)*c_[0]+c_[1]
        line['TotalScore'] = line['TotalScore']+line[key+'Score']
'''
数据检查
'''
AA = np.array(sorted(get_by_key(dic_ClusterChara,'TotalScore')))

'''
输出
'''
Road_IDs = []
for key,value in dic_ClusterChara.items():
    Road_IDs.append(key)
A = ['SD_Green','Pano_per_k','WIDTH_infer','HEIGHT1','HEIGHT2'
    ,'KGB1','KGB2','CONTINUE1','CONTINUE2','var_height','Var_HbyA']
B = ['TotalScore','Nature','City','Flow','Passage','Noise']
lenB = len(B)
for i in range(lenB):
    if i != 0:
        B.append(B[i]+'Score')

for line in data['features']:
    line = line['attributes']
    key = str(line['Green_Matlab'])
    if key in Road_IDs:
        for i in range(len(A)):
            line[A[i]] = dic_ClusterChara[key][B[i]]
    else:
        line['Green_Matlab'] = -1
        line['SD_Green'] = 0
        line['Pano_per_k'] = 0
        line['WIDTH_infer'] = 0
        line['HEIGHT1'] = 0
        line['HEIGHT2'] = 0
        line['KGB1'] = -1
        line['KGB2'] = -1
        line['CONTINUE1'] = -1
        line['CONTINUE2'] = -1
        line['var_height'] = -1

for i in range(len(A)):
    data['fieldAliases'][A[i]] = B[i]
for line in data['fields']:
    if line['name'] in A:
        line['alias'] = B[A.index(line['name'])]

fp = open('StV_Lin_Kmns_Score.json','w')
json.dump(data,fp)
fp.close()
print('After processing 2 finished')