from urllib import request
from urllib import parse
import  http.cookiejar as coo



url = "https://baijia.baidu.com/";
user_agent = "Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/57.0"

value = {"username":"wangtan", "password":"123456" }
heards = {'User-Agent':user_agent, 'Referer': 'https://news.qq.com/a/20171220/004228.htm'}
data = parse.urlencode(value)

req = request.Request("https://baijia.baidu.com/")

request.urlopen("").re

try:
    request.urlopen(req)
except request.HTTPError as e:
    print(e.code)
except request.URLError as e:
    print(e.reason)
else:
    print("OK")

#声明一个CookieJar对象实例来保存cookie
cookie = coo.CookieJar()
#利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
handler=request.HTTPCookieProcessor(cookie)
#通过handler来构建opener
opener = request.build_opener(handler)
#此处的open方法同urllib2的urlopen方法，也可以传入request
response = opener.open('https://baijia.baidu.com/')
for item in cookie:
    print ('Name = '+item.name)
    print ('Value = '+item.value)
