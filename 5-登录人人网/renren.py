#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""实现人人网登录"""

import requests

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
}

cookies = """anonymid=jajr924z-jj69zk; _r01_=1; depovince=GW; ick_login=28492155-4ea9-474c-9db2-b40b986fc353; JSESSIONID=abcNahUTubUJQ7LnRrpMw; first_login_flag=1; ln_uact=437891878@qq.com; ln_hurl=http://head.xiaonei.com/photos/0/0/men_main.gif; wp=0; wp_fold=0; jebecookies=26a27199-7e8d-47d4-a687-9f84ee6a234b|||||; _de=6459161D5831F4DC72FFEFECAA50653A696BF75400CE19CC; p=5ed1fa1cc0f5c976b1e38e906640d2202; t=38c6ac41ef90f3530492c2a8e055efdd2; societyguester=38c6ac41ef90f3530492c2a8e055efdd2; id=719382012; ver=7.0; xnsid=70acf71e; loginfrom=null"""

# 除了在headers中增加cookies字段, 也可以把cookies变成字典,放到函数中
cookies = {i.split("=")[0]:i.split("=")[1] for i in cookies.split("; ")}

post_url = "http://www.renren.com/PLogin.do"
# 不一定要用户名密码登录, 也可以直接用cookie登录
# post_data = {
#     "email": "xxxxx@xxxx.com",
#     "password": "xxxxx"
# }

s = requests.session()
# 先把cookie保存好
# response = s.post(post_url, headers=headers)
# 然后再获取内容
r = s.get("http://www.renren.com/719382012/profile", headers=headers, cookies=cookies)
print(r.content.decode())