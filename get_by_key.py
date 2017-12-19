def get_list_by_key(data,key):
    Out=[]
    for line in data:
        line = line['attributes']
        Out.append(line[key])
    return Out