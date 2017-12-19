
import json

path="StreetViewPictures_point_Seg.json"
with open(path,'r') as f:
    alldata=json.load(f)
f.close()
data=alldata['features']

from get_by_key import get_list_by_key
Tree = get_list_by_key(data,'Tree')
max = max(Tree)
min = min(Tree)
print('none')