import pandas as pd
from pyecharts import Line
import copy

df=pd.read_excel("commentsList_cleaned.xlsx",encoding="gb2312")


#2018-08-08 09:11:59
df["time_ymd"]=df["time"].apply(lambda x:x[:10])
# print(df.head())


perDayCount=df.groupby("time_ymd")["cmntcount"].count()

line=Line("每日评论数")
line.add("日期",perDayCount.index,perDayCount.values,line_type="dotted")
line.render("每日评论变化折线图.html")



df["time_mdh"]=df["time"].apply(lambda x:x[:13])
grouped=copy.deepcopy(df.groupby("time_mdh"))
perHourCount=grouped["cmntcount"].count()
line=Line("每小时评论数")
line.add("小时",perHourCount.index,perHourCount.values,line_type="dotted",is_datazoom_show=True)
line.render("每小时评论变化折线图.html")











