import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from pyecharts import Bar,Line,Overlap



df=pd.read_excel("Comments_qzq2514_20180819.xlsx",encoding="gb2312")
# print(df.shape)   #(3000, 6)即3000行数据，6个属性
#
# print(df[df.duplicated(subset=["nick","content"])].shape)   #根据指定字段显示每一行是否有重复的(21, 5)
#删除重复行(这里"nick"和"content"属性都相同的则视为重复，keep选择保留第一个，inplace=True表明在原数据表上修改)
df.drop_duplicates(subset=["nick","content"],keep="first",inplace=True)
print(df.shape)   #(2979, 5)   #删除重复行后只留下2919行


#字符串形式的日期转换成日期类型
#"2018-08-09 15:32:27"
def time2stamp(cmnttime):
    cmnttime=datetime.strptime(cmnttime,"%Y-%m-%d %H:%M:%S")
    stamp=int(datetime.timestamp(cmnttime))
    return stamp

# print(time2stamp("2018-08-09 15:32:28"))

#生成新列"stamp",其是时间列的时间戳
df["stamp"]=df["time"].apply(time2stamp)
# print(df.head(5))
#

#根据评论时间排序,并增加一列，表示包括该评论前的总评论数
df=df.sort_values(by="stamp").reset_index(drop=True)
df["cmntcount"]=df.index+1
# print(df.head())

#保存清洗后的数据
df.to_excel("commentsList_cleaned.xlsx",encoding="gb2312",index=False)


plt.plot(df.stamp,df.cmntcount)
plt.show()              #简单画出评论数随时间变化图


df["time_mdh"]=df.time.apply(lambda x:x.split(":")[0][5:])   #截取时间中的月日和时间，例如08-09 15:32:28
df_mdhmax=df.groupby("time_mdh")["cmntcount"].max()      #得到截止到该小时的总评论数
df_mdhcount=df.groupby("time_mdh")["cmntcount"].count()
#df.groupby()返回一个元素是tuple的DataFrameGroupBy，tuple第一个元素是按照分组的那个值，这里就是time_mdh，tuple第二个元素是该组下的
#DataFrame(原DataFrame除去time_mdh一列)
#df.groupby("time_mdh")["cmntcount"]返回的是每个元素是tuple的SeriesGroupBy，tuple第一个元素是按照分组的那个值，即time_mdh
#第二个元素就是该组下的["cmntcount"]，就相当于df.groupby()每组中的DataFrame都只保留"cmntcount"列
#追后加上.count()返回一个Series，index是每组的"time_mdh"，values就是得到以time_mdh分组后每组的"cmntcount"列的个数


#使用pyecharts显示图片
print(type(df_mdhcount))
bar=Bar("每小时评论数")
#is_datazoom_show参数是的图像具有变焦效果
bar.add("小时",df_mdhcount.index,df_mdhcount.values,is_label_show=True,xaxis_interval=-90,
        xaxis_rotate=-90, yaxis_interval=200,yaxis_max=800,is_datazoom_show=True)

line=Line("总评论数")
line.add("小时", df_mdhmax.index, df_mdhmax.values,line_opacity=1,
         line_type='dotted', yaxis_interval=1000,yaxis_max=4000)

#单独显示一个柱状图或者条形图，直接bar.reder()或者line.render()，如果要在同一张图中显示不同类型的图，需要Overlap进行堆叠
overlap=Overlap()
overlap.add(bar)
overlap.add(line,is_add_yaxis=True,yaxis_index=1)
overlap.render()                #渲染生成html，并在浏览器中打开才能看到图片
