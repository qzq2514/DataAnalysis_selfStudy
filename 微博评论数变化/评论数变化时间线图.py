import pandas as pd
from pyecharts import Line,Geo,Timeline
import numpy as np
from urllib import request
from bs4 import BeautifulSoup
import json
import copy

df=pd.read_excel("commentsList_cleaned.xlsx",encoding="gb2312")

#下面是绘制动态的时间线图
path="/anaconda3/envs/python36_Anaconda/lib/python3.6/site-packages/pyecharts/datasets/city_coordinates.json"
def getProvinces():
    url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/"
    header = {
        'Cookie': 'AD_RS_COOKIE=20081932; _trs_uv=jld9oaj0_6_4aho; _trs_ua_s_1=jld9oaj0_6_k1mh',
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"}

    # 有时候会网站会为了防止爬虫而设置一些机制，我们就必须要使用带有请求头的Request进行访问网址，而不能仅仅通过一个url
    # 不然会报错:urllib.error.HTTPError: HTTP Error 404: Not Found
    html = request.urlopen(request.Request(url=url, headers=header)).read().decode("gb2312")
    soup = BeautifulSoup(html, "lxml")
    # print(soup.prettify())     #按照树形打印html源码

    provinces = []
    getTrs = soup.find_all("tr", {"class": "provincetr"})  # 根据指定的属性找到指定的标签
    for tr in getTrs:
        for a in tr.find_all("a"):
            txt = a.get_text()
            if txt == "内蒙古自治区" or txt == "西藏自治区":
                txt = txt[:-3]
            elif txt == "新疆维吾尔自治区" or txt == "宁夏回族自治区" or txt == "广西壮族自治区":
                txt = txt[:2]
            else:
                txt = txt[:-1]
            provinces.append(txt)
    return provinces

provincesList=getProvinces()


#处理"city_coordinates.json"文件中不存在的地区
def handleJson(addr):
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

#根据表格中的日期进行处理
def handleArea(addr):
    tempS=addr
    if addr[:2] in provincesList:
        tempS =addr[2:]
    elif addr[:3] in provincesList:
        tempS = addr[3:]
    else:                   #三个字锁着前两个字都不是省，说明是国外，返回空
        return np.NaN

    res=""
    if tempS=="":
        res= addr            #防止只有一个省份
    else:
        res= tempS

    handleJson(res)
    return res

timeline = Timeline(is_auto_play=False, timeline_bottom=0)

df["time_ymd"]=df["time"].apply(lambda x:x[:10])
grouped=copy.deepcopy(df.groupby("time_ymd"))    #根据日期进行分组

for single in grouped:
    date=single[0]
    dff = pd.DataFrame()
    # dff=single[1]
    # print(dff.loc[:,"area"])
    dff.loc[:,"area"]=single[1].loc[:,"area"].apply(handleArea)
    dff.dropna(axis = 0)
    arr=dff.groupby("area")["area"].count()   #该时间段的每个地区的评论数,返回Series,index是每组的"area"，values是评论数
    # attr=dff.groupby("area")
    # print(type(arr))
    tempGeo=Geo("%s日评论数"%date,"“中国年轻人正带领国家走向危机”，这锅背是不背？",
         title_color="#fff",title_pos="center",width=1200,height=600,
         background_color="#404a59")
    # print(arr.values)
    tempGeo.add("",arr.index,arr.values,is_visualmap=True)
    timeline.add(tempGeo,"%s"%date)
    # print(single[1])

timeline.render("时间线图.html")