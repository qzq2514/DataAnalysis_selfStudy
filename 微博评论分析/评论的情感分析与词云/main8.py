import pandas as pd
from snownlp import SnowNLP
import jieba.analyse
import jieba
import numpy as np
import matplotlib.pyplot as plt
from pyecharts import WordCloud

#现根据评论生成每句评论的情感，保存成一个文件
# df=pd.read_excel("commentsList.xlsx",encoding="gb2312")
#
# def getSentiment(cont):
#     s=SnowNLP(cont)
#     return s.sentiments  #返回评论的情感评分，处于0-1之间，越接近1越正面
#
# df["sentiment"]=df["content"].apply(getSentiment)
#
# df_sentiment=df[["content","sentiment"]]
#
# df_sentiment=df_sentiment.sort_values(by=["sentiment"],ascending=False)
#
# df_sentiment.to_excel("sentimentList.xlsx",index=False,encoding="gb2312")

df_sentiment=pd.read_excel("sentimentList.xlsx",encoding="gb2312")
all_content=df_sentiment["content"].values.tolist() #把所有评论放在一个list中
# print(type(all_content))

contented_content=" ".join(all_content)   #把list中的句子合并成一个大句子

#基于TF-IDF算法的关键词抽取，参数依次表示分析的句子，返回的TF/IDF权重最高的几个关键词，后面两个参数不必过于理睬应该是与TF/IDF算法有关的
#该方法返回关键词的集合
extract_tagsList=jieba.analyse.extract_tags(contented_content,topK=200,withWeight=False,allowPOS=("ns","n"))
extract_tags=" ".join(extract_tagsList)
# print(extract_tags)

afterCut=jieba.lcut(contented_content)
countlist=[]
for tags in extract_tagsList:
    countlist.append(afterCut.count(tags))   #python的list的append方法会修改本身，不需要再赋值给本身


tagsCount=pd.Series(data=countlist,index=extract_tagsList).sort_values(ascending=False)

# print(tagsCount)
#绘制词云
wordCloud=WordCloud(width=800,height=520)
wordCloud.add("评论词云",tagsCount.index,tagsCount.values,shape="cardioid",word_size_range=[20,100])
wordCloud.render("评论词云.html")