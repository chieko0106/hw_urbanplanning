
import json

path="StreetViewPictures_point_Seg.json"
with open(path,'r') as f:
    alldata=json.load(f)
f.close()
data=alldata['features']

from Tools import get_list_by_key
Tree = get_list_by_key(data,'Tree')


import scipy
points=scipy.randn(20,4)
print('none')