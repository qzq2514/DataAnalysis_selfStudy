import operator

# python3没有cmp函数，使用operator比较list或者数值或元组
print(operator.lt(["a","c","d"],["a","r","e"]))  #小于
print(operator.gt(["1","2","3"],["1","3","2"]))  #大于
#还有le(小于等于),ge(大于等于),eq(等于)

arr=["a","d","b","n","d"]
print(sorted(arr))  #list排序

print(arr.count("d"))  #指定元素出现的次数

arr.extend(["1","2"])  #将数组拆分并将其中的元素全部添加到arr后面
arr.extend("qzq")      #extend参数必须是数组，所以传进去的字符串被分解成字符数组
print(arr)             #与append不同，append是简单将参数元素添加到arr后面(无论其是不是数组)
