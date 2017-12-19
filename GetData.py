import json
import numpy
path="StreetViewPictures_point_Seg.json"
with open(path,'r') as f:
    alldata=json.load(f)
    f.close()
data=alldata['features']

from Tools import get_list_by_key
Tree = get_list_by_key(data,'Tree')

all_keys = data[0]['attributes']
All_keys=[]
for key, value in all_keys.items():
    All_keys.append(key)

from Tools import ArrangeData4HierarchicalClustering
Points = ArrangeData4HierarchicalClustering(data,All_keys[15:26])

with open('Out.json','a') as f:
    json.dump({'Points':Points},f)
    f.close()
print('Get data finished')

