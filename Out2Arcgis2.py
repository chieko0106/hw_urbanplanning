# -*- coding:utf-8 -*-
import json
path="StreetViewPictures_point_Seg.json"
with open(path,'r') as f:
    alldata=json.load(f)
    f.close()
with open('Out.json','r') as f:
    newdata=json.load(f)
    f.close()

n = 0
for item in newdata:
    item = item['attributes']
    nn = 15
    for key,value in item.items():
        all_data_key = alldata['fields'][nn]['name']
        alldata['fields'][nn]['alias'] = key
        alldata['fieldAliases'][all_data_key] = key
        alldata['features'][n]['attributes'][all_data_key] = value
        nn = nn+1
        if key == 'Cluster':
            break
    n = n+1

fp = open('St_View_Point_Kmeans_2.json','w')
json.dump(alldata,fp)
fp.close()

from Tools import get_list_by_key
Cluster = get_list_by_key(alldata['features'],'Pavement')
print('Out2Arcgis2 finished')