# import numpy as np
a=(1,2,3)        #被zip的可以是tuple,也可以是list,也可以是list的list
b=[4,5,6]
c=[[7],[8],[9]]
zz=zip(a,b,c)
for var1 in list(zz):    #被压缩的list相同位置的元素组成一个tuple
    print(var1)

print("--------")
x,y,z=zip(*zip(a,b,c))   #zip的逆过程
print(x)
print(y)
print(z)

# 输出：
# [(1, 4, 7), (2, 5, 8), (3, 6, 9)]
# (1, 2, 3)
# (4, 5, 6)
# (7, 8, 9)