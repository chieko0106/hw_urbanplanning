
import json

path="StreetViewPictures_point_Seg.json"
with open(path,'r') as f:
    alldata=json.load(f)
f.close()
data=alldata['features']

print('none')