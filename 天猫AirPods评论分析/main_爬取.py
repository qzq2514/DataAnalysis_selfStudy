import requests
import json
import pandas as pd
import time
import random


class ReptilianUtil(object):
   def __init__(self,itemId):
       self.itemId=itemId
       self.header={
           'Accept':'*/*',
           'Accept-Encoding':'gzip, deflate, br',
           'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
           'user-agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
       }
       self.maxPageNum =self.getLastPage()
       self.table=pd.DataFrame(columns=["customID","displayUserNick","auctionSku","rateContent","rateDate"])
       self.customId=1

   def getdictFromPage(self,page):
       url = "https://rate.tmall.com/list_detail_rate.htm?itemId={}&spuId=700188114&sellerId=" \
                 "1669409267&order=3&currentPage={}&append=0&content=1&tagId=&posi=&picture=&groupId=&ua&needFold=0&_ksTS=1540796467894_398" \
                 "&callback=jsonp399".format(self.itemId, page)   #根据商品的ID和指定的第几页，得到该商品该页的评论HTML

       timeout=random.choice(range(80,180))
       reponse=requests.get(url,headers=self.header)

       html =reponse.text           #得到指定页的商品评论html
       print("page-----------------", page)
       if html.find("jsonp399")==-1:   #处理异常的返回值(有时候可能会返回整个网页的html，而不是json形式的)
           print("Error Dict~")
           return dict()

       # 对得到的字符串进行预处理，保证是合法的json形式
       html =html.replace("false",'"false"')
       html =html.replace("true", '"true"')
       html = html.replace('jsonp399(', '')
       html = html.replace(')', '')

       print(html)
       tMallJson=json.loads(html)

       return tMallJson        #返回该页商品的dict信息，详见“json结构.png”

    #根据第一页的初始化信息，得到该商品总共有多少页评论
   def getLastPage(self):
       txt1Page=self.getdictFromPage(1)
       return txt1Page['rateDetail']['paginator']['lastPage']

   #得到该商品的所有购买信息，每条购买信息包括商品套餐类型(auctionSku),购买者昵称(displayUserNick),评论(rateContent),购买时间(rateDate)
   def getFullInfo(self):
       # for curPage in range(1,self.maxPageNum+1):
       for curPage in range(1, self.maxPageNum+1):
           curFullDict=self.getdictFromPage(curPage)
           if len(curFullDict)==0: continue

           rateDetail=curFullDict["rateDetail"]
           rateList=rateDetail["rateList"]
           for curCmt in rateList:
               auctionSku = curCmt["auctionSku"]
               displayUserNick = curCmt["displayUserNick"]
               rateContent = curCmt["rateContent"]
               rateDate = curCmt["rateDate"]
               print(auctionSku+"--"+displayUserNick+"--"+rateContent+"--"+rateDate)

               self.table=self.table.append({"customID":self.customId,"displayUserNick":displayUserNick,
                                  "auctionSku":auctionSku,"rateContent":rateContent,"rateDate":rateDate},ignore_index=True)
               self.customId += 1

           if curPage % 5 == 0:
               time.sleep(random.randint(5, 10))
       return self.table

if __name__=='__main__':
       Reptilian=ReptilianUtil(548541598821)
       cmtTable=Reptilian.getFullInfo()
       cmtTable.to_excel("Comments_AirPods.xlsx",index=False,encoding="gb2312")

