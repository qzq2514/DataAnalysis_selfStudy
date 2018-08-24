import requests
import time
import random
import  json
import pandas as pd
import  openpyxl

#jsvar=loader_1534681413266_87398998
comments=pd.DataFrame(columns=["page","nick","area","time","content"])

try:
    for page in range(0,5):
        start=int(time.time())*1000   #time()返回当前时间的时间戳（1970纪元后经过的浮点秒数）--整数部分10位
        end_stamp=start+random.randint(100,1000)
        end=str(end_stamp)[-8:]     #根据jsvar的参数看出后面的终点时戳是八位int
        url="http://comment5.news.sina.com.cn/page/info?version=1&format=js&channel=cj&newsid=comos-hhkuskt2879316&group=0&compress=0&ie=gbk&oe=gbk&" \
            "page={}&page_size=20&jsvar=loader_{}_{}".format(page,start,end)
        r=requests.get(url).text
        # print(r[34:])
        json_dict=json.loads(r[34:])    #json.loads()根据字符串加载json
        cmntlist=json_dict["result"]["cmntlist"]     #根据"微博评论json图"找到评论集合
        replydict=json_dict["result"]["replydict"]
        # comments=comments.append({"page":page+1,"nick":json_dict,"cmntlist":cmntlist,"replydict":replydict},ignore_index=True)
        for num,cmnt in enumerate(cmntlist):
            print(page*20+num+1,page+1,cmnt["nick"],cmnt["area"],cmnt["time"],cmnt["content"])
            comments = comments.append({"page":page+1,"nick":cmnt["nick"],"area":cmnt["area"],
                                        "time":cmnt["time"],"content":cmnt["content"]},ignore_index=True)
        if page%5==0:
            time.sleep(random.randint(0,2))
except:
    print("Error")


# comments.to_csv("Sina_Finance_Comments_qzq2514_20180819.csv",index=False,encoding="gb2312")
comments.to_excel("Sina_Finance_Comments_qzq2514_20180819.xlsx",index=False,encoding="gb2312")
# print(random.randint(100,1000))


