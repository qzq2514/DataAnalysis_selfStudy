import pandas as pd
import json
import time
import requests
import random
from lxml import etree


df = pd.read_excel('complexComments_qzq2514_20180819.xlsx',encoding='gb2312')
# print(df.head(10))

# cmntlist=df.cmntlist.values.tolist()
# print(len(cmntlist))
# print(type(cmntlist[0]))
# print(cmntlist[0][:200])



# df["jsons"]=df.jsons.apply(lambda x:eval(x))
#将字符串形式的数据通过eval()函数变成有效的表达式，这里变成字典形式
df["cmntlist"]=df.cmntlist.apply(lambda x:eval(x))
# df["replydict"]=df.replydict.apply(lambda x:eval(x))
# print(df.head(10))

#cmntlists中每个元素是每页20个评论构成的该页评论的集合，cmntlists长度是椰树
cmntlists=df["cmntlist"].values.tolist()
# print(len(cmntlists),len(cmntlists[0]),cmntlists[0][0])

#sum将元素是list的集合中的list元素拆开成再组合成一个大集合，eg:sum([[1,2],[3,2,1]], [])    ->[1, 2, 3, 2, 1]
cmntlist=sum(cmntlists,[])
# print(len(cmntlist))    #每页的20个评论全部拆开成一个大集合cmntlist,cmntlist的长度就是页数*每页评论数=150*20=3000
# print(type(cmntlist))   #<class 'list'>
# print(json.dumps(cmntlist[0], ensure_ascii=False, indent=0))   #竖向格式化打印dict

# for num,cmnt in enumerate(cmntlist):   #enumerate()函数返回可迭代对象的迭代器,每个元素是一个长度为2tuple,
#     print(cmnt["ip"],cmnt["area"])     #每个tuple第一个元素是编号，第二个元素是原迭代对象的元素
#     if num==10:break                        #打印前十个评论的ip地址和物理地址

# for cmnt in cmntlist:                 #这种迭代没有编号
#     print(cmnt["ip"], cmnt["area"])

#将ip地址转换为物理地址，使用https://ip.cn网址

#由ip地址得到物理地址
def ip2loc(ip):
    url="https://ip.cn/index.php?ip={}".format(ip)
    text=requests.get(url).text
    html=etree.HTML(text)
    # 右键“审查元素 -> 点新窗口左上角的鼠标logo ->然后选中网页内容后会自动定位到源代码里位置
    # -> 右键 ‘Copy’ -> ‘Copy Xpath’，自动生成路径，这里我复制过来的是：//*[@id="result"]/div/p[2]/code
    # 代表的是整个<code>标签，后面还要加text()才能得到里面的标签内容
    #这里使用try块防止出现ip查询结果为空
    try:
        loc = html.xpath('//*[@id="result"]/div/p[2]/code/text()')[0]
    except:loc=""
    try:
        tele = html.xpath('//div[@id="result"]/div/p[4]/text()')[0]
    except:tele=""
    try:
        geo_ip = html.xpath('//div[@id="result"]/div/p[3]/text()')[0]
    except:
        geo_ip = ""
    return loc+'*'+tele+'*'+geo_ip

#测试
# for num,cmnt in enumerate(cmntlist):
#     ip_loc=ip2loc(cmnt["ip"])
#     # print(num,cmnt["ip"],cmnt["area"],ip_loc)
#     if num%5==0:
#         time.sleep(random.randint(0,2))    #设置间隔时间，以免对IP查询网站造成侵扰
#     if num==30:break

IPtable=pd.DataFrame(columns=['No','page','nick','time','content','area',
                              'ip','ip_loc','length','against','agree', 'channel',
                              'hot', 'level', 'login_type', 'media_type', 'mid'])

page=1
for num,cmnt in enumerate(cmntlist):
    nick = cmnt['nick']
    times = cmnt['time']           #一系列的数据提取
    content = cmnt['content']
    area = cmnt['area']
    ip = cmnt['ip']
    ip_loc = ip2loc(cmnt['ip'])
    length = cmnt['length']
    against = cmnt['against']
    agree = cmnt['agree']
    channel = cmnt['channel']
    hot = cmnt['hot']
    level = cmnt['level']
    login_type = cmnt['login_type']
    media_type = cmnt['media_type']
    mid = cmnt['mid']
    print(num + 1, page, times, nick, content, area, ip_loc)
    IPtable = IPtable.append(
        {'No': num + 1, 'page': page, 'nick': nick, 'time': times, 'content': content, 'area': area,
         'ip': ip, 'ip_loc': ip_loc, 'length': length, 'against': against, 'agree': agree,
         'channel': channel, 'hot': hot, 'level': level, 'login_type': login_type,
         'media_type': media_type, 'mid': mid}, ignore_index=True)
    # if num % 30 == 0:
    #     time.sleep(random.randint(0, 1))
    if num==10:break        #提取十个信息展示下
    if int((num+1)%20) == 0:
        page += 1

print(len(IPtable))
IPtable.to_excel("ipTable.xlsx",index=False,encoding="gb2312")