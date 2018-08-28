import requests
from urllib import request
from bs4 import BeautifulSoup

url="http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/"
header = {
    'Cookie': 'AD_RS_COOKIE=20081932; _trs_uv=jld9oaj0_6_4aho; _trs_ua_s_1=jld9oaj0_6_k1mh',
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"}

#有时候会网站会为了防止爬虫而设置一些机制，我们就必须要使用带有请求头的Request进行访问网址，而不能仅仅通过一个url
#不然会报错:urllib.error.HTTPError: HTTP Error 404: Not Found
html=request.urlopen(request.Request(url=url,headers=header)).read().decode("gb2312")
soup = BeautifulSoup(html,"lxml")
# print(soup.prettify())     #按照树形打印html源码

provinces=[]
getTrs=soup.find_all("tr",{"class":"provincetr"})    #根据指定的属性找到指定的标签
for tr in getTrs:
    for a in tr.find_all("a"):
        txt=a.get_text()
        if txt=="内蒙古自治区" or txt=="西藏自治区":
            txt=txt[:-3]
        elif txt=="新疆维吾尔自治区" or txt=="宁夏回族自治区" or txt=="广西壮族自治区":
            txt=txt[:2]
        else: txt=txt[:-1]
        provinces.append(txt)     #获取省份信息

print(provinces)