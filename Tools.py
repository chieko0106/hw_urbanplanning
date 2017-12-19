#从data里面按照key提取所有POI的key的value组成新的数组
def get_list_by_key(data,key):
    Out=[]
    for line in data:
        line = line['attributes']
        Out.append(line[key])
    return Out
#将data里的数据重新整理,用于层次聚类

import json
def ArrangeData4HierarchicalClustering(Data,All_keys):
    Out = []
    Element = []
    for line in Data:
        line = line['attributes']
        for key in All_keys:
            Element.append(line[key])
        Out.append(Element)
        if len(Out)%1000 == 0:
            print(len(Out)/1000)
    return Out