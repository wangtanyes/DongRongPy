import sys
sys.path.append("D:\\Python Project\\MyfirstPython\\firstRex.py")

import firstRex as a



import  re

s = r"abc"



# # print(re.findall(s,"abc"))
#
# st = "top tip tqp twp tep";
# res = r"top"
# print(re.findall(res, st))
#
# # 符合tip 与top 的都可以
#
# res=r"t[io]p"
# print(re.findall(res, st))
#
# #  res=r"t[^io]p"  其中^是取反的意思，是不包含io的， 当[io$]或者[io^]时，$与^不起作用的,方括号中也可以用[a-zA-Z0-9]
# res = r"t[^io]p"
# print(re.findall(res, st))
#
#
# s= "hello world, hello boy"
#
# # 匹配开头出现hello的字符
# r1= r"^hello"
# print(re.findall(r1, s))
#
# # 匹配行位出现boy的字符
# r2 = r"boy$"
# print(re.findall(r2, s))

