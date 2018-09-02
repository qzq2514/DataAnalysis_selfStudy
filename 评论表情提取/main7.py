import pandas as pd
import re
from collections import Counter
from pyecharts import Bar
import jieba
from nltk.draw.dispersion import dispersion_plot
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False


import nltk

df=pd.read_excel("commentsList.xlsx",encoding="gb2312")

#评论表情柱状图
def getEmoji(content):
    #[中国赞],下面正则表达式中前后两个反斜杠分别转义前后的中括号
    #而\u4e00-\u9fa5是所有汉字的unicode编码范围
    patt=re.compile(u"\[[a-zA-Z\u4e00-\u9fa5]+\]")
    result=re.findall(patt,content)   #找到评论中所有的emoji,返回元素是字符串的列表
    return result

df["emoji_list"]=df.content.apply(getEmoji)

# print(df.head(10)["emoji_list"])

emojis=df["emoji_list"].values#.tolist()   #values获得Series的值,这里df["emoji_list"]中每个元素值是一个list
# print(type(emojis))

emojis_list=sum(emojis,[])   #将集合元素是list的emojis中的每个list拆开合并成一个大list
emojis_set=list(set(emojis_list))   #先转为set,得到有多少种表情，然后转为list，便于后面操作
# num=len(emojis_set)
# print(num)
# print(emojis_set)

counter=Counter(emojis_list)
# print(counter.most_common())

x_emojis,y_counts=zip(*counter.most_common())  #counter.most_common()是元素是tuple的list,*将list拆开，变成一个个tuple,然后相同位置的tuple组成一个大tuple
                                       #counter.most_common()是list,每个元素是长度为2的tuple,第一个位置表示表情，第二个位置表示个数
                                       #zip就负责将多个list或者tuple的相同位置的元素组成一个大list
# print(type(x_emojis))       ---第一个位置表示表情,这里x_emoji就表示表情字符串的集合

bar=Bar("emoji使用情况")
bar.add("emoji",x_emojis[:20],y_counts[:20],is_stack=True,is_label_show=True,xaxis_interval=0,xaxis_rotate=-45,xaxis_margin=8)

bar.render("emoji使用情况.html")



#评论数据-nltk分布图谱
comments_list=df["content"].values
cmnts=" ".join(comments_list)       #全部评论放在一个字符串里
print(len(cmnts))

emoji_droped=[]

# print(x_emojis)     #('[doge]', '[二哈]'........)
for emoji in x_emojis:
    emoji=emoji[1:-1]  #去掉中括号
    jieba.add_word(emoji)
    emoji_droped.append(emoji)


#jieba.cut对字符串进行分词
# cut_all=True全模式：试图将句子最精确地切开，适合文本分析，输出的是所有可能的分词组合，比如清华大学，会被分成：清华，清华大学，华大，大学
# cut_all=False默认模型（精确模型）：把句子中所有的可以成词的词语都扫描出来, 速度非常快，但是不能解决歧义，比如清华大学，只会输出清华大学
#还有个分词函数:jieba.cut_for_search
# 搜索引擎模式：在精确模式的基础上，对长词再次切分，提高召回率，适合用于搜索引擎分词
words=list(jieba.cut(cmnts, cut_all=False))
# print(len(words))
# print(words)
# print(emoji_droped)


ntext=nltk.Text(words)
ntext.dispersion_plot(emoji_droped[:15])       #出现中文不显示的问题



