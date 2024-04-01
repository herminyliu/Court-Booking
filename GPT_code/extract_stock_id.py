import json

# 这是你提供的响应体的字符串表示
response_body = '''{"backObject":null,"message":null,"object":
[{"PRICE":"20.00","SURPLUS":1,"USING_NUM":1,"SERVICEID":"301","ID":272844,"REMARK":"兴庆校区东南网球场","TIME_NO":"16:01-17:00","STATUS":1,"ISOVER":1,"ALL_COUNT":2},
{"PRICE":"20.00","SURPLUS":2,"USING_NUM":0,"SERVICEID":"301","ID":272845,"REMARK":"兴庆校区东南网球场","TIME_NO":"17:01-18:00","STATUS":1,"ISOVER":1,"ALL_COUNT":2}],"reason":null,"result":"1"}'''

# 解析 JSON 数据
data = json.loads(response_body)

# 提取所需信息
for item in data['object']:
    if item['TIME_NO'] == '16:01-17:00':
        tennis_court_id = item['ID']
        print("网球场 ID:", tennis_court_id)
