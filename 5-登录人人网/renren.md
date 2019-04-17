# 1. 方法一, 用session先发送post请求,登录后session自动保存cookie,然后再同session获取登陆后内容

# 2. 方法二, 在headers中增加cookie字段

# 3. 方法三, 将cookie字段转化为字典, 放到requests.get的函数参数中