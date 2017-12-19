# -*- coding:utf-8 -*-
import json
path="StreetViewPictures_point_Seg.json"
with open(path,'r') as f:
    alldata=json.load(f)
    f.close()
with open('Out.json','r') as f:
    newdata=json.load(f)
    f.close()

dataslice = newdata[0]['attributes']
Aliases = {}
fields = []
for key, value in dataslice.items():
    Aliases[key] = key
    fields.append({'name':key,'type':'esriFieldTypeDouble','alias':Aliases[key]})
    if key == 'OBJECTID':
        fields[-1]['type'] = 'esriFieldTypeOID'
    elif key in ['Value_','LineOID','CV']:
        fields[-1]['type'] = 'esriFieldTypeString'
        fields[-1]['length'] = 255
        if key == 'CV':
            fields[-1]['length'] = 2000
    elif key in ['pointID','ROAD_ID','pano_id']:
        fields[-1]['type'] = 'esriFieldTypeInteger'

alldata['features'] = newdata
alldata['fields'] = fields
alldata['fieldAliases'] = Aliases
fp = open('St_View_Point_Kmeans.json','w')
json.dump(alldata,fp)
fp.close()
print('Out2Arcgis finished')