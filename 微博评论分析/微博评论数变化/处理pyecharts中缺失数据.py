import json
import copy

lst=["崇左","塘沽","睢宁","广安","东城","达州"]

path="/anaconda3/envs/python36_Anaconda/lib/python3.6/site-packages/pyecharts/datasets/city_coordinates.json"


def handleArea(addr):
    with open(path,"r",encoding='utf-8') as fr:
        dataDict=json.loads(fr.read())

        data_new=dataDict.copy()
        for key in dataDict.keys():
            if(key==addr):break
            if key.startswith(addr):
                data_new[addr]=dataDict[key]
                break

    with open(path,"w",encoding='utf-8') as fw:
        fw.write(json.dumps(data_new,ensure_ascii=False))



for addr in lst:
    handleArea(addr)



