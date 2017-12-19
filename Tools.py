# -*- coding:utf-8 -*-
#从data里面按照key提取所有POI的key的value组成新的数组
def get_list_by_key(data,key):
    Out=[]
    for line in data:
        line = line['attributes']
        Out.append(line[key])
    return Out
#将data里的数据重新整理,用于层次聚类

import json
import numpy as np
def Data4HC(Data,All_keys):
    Out = []
    for line in Data:
        Element = []
        line = line['attributes']
        for key in All_keys:
            Element.append(np.array(line[key]))
        Out.append(Element)
        if len(Out)%1000 == 0:
            print(len(Out)/1000)
    Out = np.array(Out)
    return Out

def Data2Interested(Data):
    Out = []
    for line in Data:
        geo = line['geometry']
        attri = line['attributes']
        new_attri = {}
        new_attri['Nature'] = attri['Sky']+attri['Tree']
        new_attri['City'] = attri['Building']+attri['Fence']
        new_attri['Flow'] = attri['Car']+attri['Pedestrian']+attri['Bicyclist']
        new_attri['Passage'] = attri['Pavement']+attri['Road']
        new_attri['Noise'] = attri['Pole']+attri['RoadMarking']+attri['SignSymbol']
        Out.append({'attributes':new_attri,'geometry':geo})
    return Out