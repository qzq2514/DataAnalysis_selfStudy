import pandas as pd
import re
import numpy as np
from pyecharts import Bar,Map,Geo


df=pd.read_excel("commentsList.xlsx",encoding="gb2312")

#提取省份
#复制过来省份信息
# prolist='北京市，天津市，上海市，重庆市，河北省，山西省，辽宁省，吉林省，江苏省，浙江省，安徽省，福建省，\
# 江西省，山东省，河南省，湖北省，湖南省，广东省，海南省，四川省，贵州省，云南省，陕西省，甘肃省，\
# 青海省，台湾省，广西，西藏，宁夏，新疆，香港，澳门，内蒙古，黑龙江省'
#
# prolist=prolist.replace("省","").replace("市","").split("，")

capital={"北京":"北京","天津":"天津","上海":"上海","重庆":"重庆","河北":"石家庄","山西":"太原","辽宁":"沈阳","吉林":"长春","江苏":"南京","浙江":"杭州",
         "安徽":"合肥","福建":"福州","江西":"南昌","山东":"济南","河南":"郑州","湖北":"武汉","湖南":"长沙","广东":"广州","海南":"海口","四川":"成都",
         "贵州":"贵阳","云南":"昆明","陕西":"西安","甘肃":"兰州","青海":"西宁","台湾":"台北","广西":"南宁","西藏":"拉萨","宁夏":"银川","新疆":"乌鲁木齐",
         "香港":"香港","澳门":"澳门","内蒙古":"呼和浩特","黑龙江":"哈尔滨"}

def getProvince(area):
    for pro in list(capital.keys()):
        if area.startswith(pro):
            return pro
    return "海外"


#根据一列生成另一列信息，使用apply
df["pro"]=df.area.apply(getProvince)
# df=df.dropna(axis = 0)
pro_count=df.groupby("pro")["nick"].count().sort_values(ascending=False)

bar=Bar("省份分布")
# bar.use_theme("macarons")  #换主题
bar.add("省份",pro_count.index,pro_count.values,is_label_show=True,xaxis_interval=0,xaxis_rotate=-45)
bar.render("评论的省份分布柱状图.html")

mapp=Map("省份分布",width=1000,height=600)
mapp.use_theme("macarons")
mapp.add("评论数",pro_count.index,pro_count.values,maptype="china",is_visualmap=True,
         visual_range=[pro_count.values.min(),pro_count.values.max()],is_map_symbol_show=False,visual_text_color="#000",is_label_show=True)
mapp.render("评论的省份分布地图.html")


def getCity(area,pro):
    res=area.replace(pro,"")
    if res=="":
        return capital[area]
    else: return res
#根据多列生成一列，使用apply或者map
#使用map提取时,python3中map返回迭代器,需要转为列表
df["city"]=list(map(getCity,df["area"],df["pro"]))

#也可以使用apply
# df["city"]=df.apply(lambda row:getCity(row["area"],row["pro"]),axis=1)

df.to_excel("commentsList_含海外.xlsx",index=False,encoding="gb2312")
#生成城市评论的柱状图
df=df[ df['pro'] != "海外"]   #删除海外评论
citiesCount=df.groupby("city")["nick"].count().sort_values(ascending=False)
bar=Bar("城市分布")                   #设置xaxis_interval保证前30个城市每个都能显示
bar.add("城市",citiesCount.index[:30],citiesCount.values[:30],is_label_show=True,xaxis_interval=0,xaxis_rotate=-45)  #生成前30个高评论城市
bar.render("评论的城市分布柱状图.html")

geo=Geo("城市分布情况","“中国年轻人正带领国家走向危机”，这锅背是不背？",title_color="#fff",title_pos="center",width=1200,height=600,
         background_color="#404a59")
geo.add("评论数", citiesCount.index, citiesCount.values, visual_range=[citiesCount.values.min(), citiesCount.values.max()], visual_text_color="#fff",
        symbol_size=10, is_visualmap=True)
geo.render("评论的城市分布地图.html")

df.to_excel("commentsList_无海外.xlsx",index=False,encoding="gb2312")