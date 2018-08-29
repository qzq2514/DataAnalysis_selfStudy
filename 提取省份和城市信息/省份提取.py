import pandas as pd
import re
from pyecharts import Bar,Map

df=pd.read_excel("commentsList.xlsx",encoding="gb2312")
#复制过来省份信息
prolist='北京市，天津市，上海市，重庆市，河北省，山西省，辽宁省，吉林省，江苏省，浙江省，安徽省，福建省，\
江西省，山东省，河南省，湖北省，湖南省，广东省，海南省，四川省，贵州省，云南省，陕西省，甘肃省，\
青海省，台湾省，广西，西藏，宁夏，新疆，香港，澳门，内蒙古，黑龙江省'
# prolist=prolist.replace('市', '').replace('省', '').split('，')

prolist=prolist.replace("省","").replace("市","").split("，")

def getProvince(area):
    for pro in prolist:
        if pro in area:
            return pro
    return "海外"
# print(prolist)

df["pro"]=df.area.apply(getProvince)
# print(df[["area","pro"]])
pro_count=df.groupby("pro")["nick"].count().sort_values(ascending=False)

# print(type(pro_count))
bar=Bar("省份分布")
# bar.use_theme("macarons")  #换主题
bar.add("省份",pro_count.index,pro_count.values,is_label_show=True,xaxis_interval=0,xaxis_rotate=-45)
bar.render("评论的省份分布柱状图.html")

mapp=Map("省份分布",width=1000,height=600)
mapp.use_theme("macarons")
mapp.add("评论数",pro_count.index,pro_count.values,maptype="china",is_visualmap=True,
         visual_range=[0,350],is_map_symbol_show=False,visual_text_color="#000",is_label_show=True)
mapp.render("评论的省份分布地图.html")

df.to_excel("commentsList1.xlsx",index=False,encoding="gb2312")