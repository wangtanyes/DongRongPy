import  re

# . 匹配除换行\n以外的字符
# \d 匹配数字，相当于[0-9]
# \D 匹配任何非数字  相当于[^0-9]
# \s 匹配空白字符  相当于类[\t\n\r\f\v]
# \S 匹配非空白字符  相当于类[^\t\n\r\f\v]
#  \w 匹配任何字母数字字符   相当于[a-zA-Z0-9]
#  \W 匹配任何非字母数字 字符  相当于^[a-zA-Z0-9]

r = r"^010-\d{8}"

# * 0次或者多次
# + 1次或者多次
#  ?  0次或者1次
# {m,n} 重复次数最少m，最多n


r2 = r"ab*"
r3 = r"ab+"
print(re.findall(r2, "abbbb"))
print(re.findall(r3, "a"))

r4 = r"csvt.net"
print(re.findall(r4, "csvt\nnet", re.S))  # 加上re.S就可以匹配“\”了

s = """
hello csvt
heoll hello
csvt hello
csvt hehe
"""

r5 = r"^csvt"
print(re.findall(r5, s, re.M))   # re.M 是多行匹配

r6=r"""
\d{3,4}
-?
\d{1}
"""
print(re.findall(r6, "010-12348", re.X))  # 当匹配的正则是多行的时候 用 re.X

r7 = r"\w{3}@\w+(\.com|\.cn)"  # (\.com|\.cn)是一个分组，表示.com或者.cn ，其中.需要转义，所以用\. ，并且分组中匹配的结果会优先返回

ss = "fimgesdfs"
print(re.search(r"img", ss).group())

print("hahhahhh", "正在进行数据验证")