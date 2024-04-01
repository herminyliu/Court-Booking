import crack_yzm_image
import crack_yzm_request


def findtime(court_id: str, book_date: str, session: str, time_no: str):
    import requests

    # 东南网球场，court_id 为301
    url = 'http://202.117.17.144/product/findtime.html'
    headers = {
        'Host': '202.117.17.144',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0',
        'Referer': 'http://202.117.17.144/product/show.html?id=' + str(court_id),
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,en-GB;q=0.6',
        'X-Requested-With': 'XMLHttpRequest',
        'Cookie': f'from=undefined; SESSION={session};'  # 尚不清楚jssessiono如何构造
    }

    # book_date按照YYYY—MM-DD格式书写
    data = {"id": str(court_id),
            "type": "day",
            "s_dates": book_date,
            "serviceid": court_id,
            # 原报文中还有一个'_'，不知到如何构造，先省略
            }

    # 需要verify=False，不然会报401错误
    r = requests.get(url=url, headers=headers, params=data, verify=False)
    jsessionid_finddate = basic_analysis_of_response(r)

    import json
    # 解析 JSON 数据
    data = json.loads(r.text)

    stock_id = "000000"
    # 提取所需信息
    for item in data['object']:
        if item['TIME_NO'].split('-')[0].split(':') == time_no.split('-')[0].split(':'):  # 这里的TIME_NO可能会有变化，所以模糊识别
            stock_id = str(item['ID'])  # 这里的ID可能会有变化

    if stock_id == "000000":
        raise Exception("++++findtime函数中的stock_id未找到！请检查输入的日期时段是否有效！++++")
    else:
        print('找到的stock_id为：' + stock_id)

    return jsessionid_finddate, stock_id


def findprice(court_id: str, book_date: str, session: str, jsessionid: str, time_no: str):
    # 其实price对于预定场地的目标不重要，但是这一步不可省略，因为我们需要获得jsessionid
    import requests

    # 东南网球场，court_id 为301
    url = 'http://202.117.17.144/product/price.html'
    headers = {
        'Host': '202.117.17.144',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0',
        'Referer': 'http://202.117.17.144/product/show.html?id=' + str(court_id),
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,en-GB;q=0.6',
        'X-Requested-With': 'XMLHttpRequest',
        'Cookie': f'from=undefined; SESSION={session}; from=undefined; JSESSIONID={jsessionid};'
    }

    # book_date按照YYYY—MM-DD格式书写
    # time_no 14:00-15:00
    data = {"type": "day",
            "s_dates": book_date,
            "serviceid": court_id,
            "time_no": time_no,
            # 原报文中还有一个'_'，不知到如何构造，先省略
            }
    r = requests.get(url=url, headers=headers, params=data, verify=False)

    jsessionid_findprice = basic_analysis_of_response(r)
    return jsessionid_findprice


def findseat(court_id: str, session: str, jsessionid: str, stock_id: str, court_num: int):
    # 其实price对于预定场地的目标不重要，但是这一步不可省略，因为我们需要获得jsessionid
    import requests

    # 东南网球场，court_id 为301
    url = 'http://202.117.17.144/seat/seat.html'
    headers = {
        'Host': '202.117.17.144',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0',
        'Referer': 'http://202.117.17.144/product/show.html?id=' + str(court_id),
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,en-GB;q=0.6',
        'X-Requested-With': 'XMLHttpRequest',
        'Cookie': f'from=undefined; SESSION={session}; from=undefined; JSESSIONID={jsessionid};'
    }

    # book_date按照YYYY—MM-DD格式书写
    # time_no 14:00-15:00
    data = {"id": court_id,
            "type": "2",  # 不知道这个值会不会变动
            "stockid": stock_id,
            "json": "html",
            # 原报文中还有一个'_'，不知到如何构造，先省略
            }

    # 需要verify=False，不然会报401错误
    r = requests.get(url=url, headers=headers, params=data, verify=False)

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(r.text, 'html.parser')
    input_tag = soup.find('input', id='txt_seatid')

    if input_tag:
        # 获取 value 属性的值
        raw_stock_detailid = input_tag['value']  # 1_2813413_3,2_2813414_1,   原始字串需要再次处理
        # 这里表示的是，某一天，某个时段所有场地的detailid号，对于羽毛球场来说，这里有10-12个场
        # 考虑到代码自用，一个时段只需要预定一个场地，网球场示例中，统一预定1号场地
    else:
        raise Exception("+++findseat函数中的stock_detailid未找到！++++")
    stock_detailid = raw_stock_detailid.split(',')[court_num].split('_')[1]
    jsessionid_findseat = basic_analysis_of_response(r)
    print('找到的stock_detailid为：' + stock_detailid)

    return jsessionid_findseat, stock_detailid


def order(court_id: str, session: str, jsessionid: str, stock_id: str, stockdetail_ids: str):
    import requests

    url = 'http://202.117.17.144/order/show.html?id=' + str(court_id)
    headers = {
        'Host': '202.117.17.144',
        'Origin': 'http://202.117.17.144',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
        'Referer': 'http://202.117.17.144/product/show.html?id=' + str(court_id),
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,en-GB;q=0.6',
        'Cookie': f'from=undefined; SESSION={session}; from=undefined; JSESSIONID={jsessionid};'
    }

    import json
    # 构造请求体数据
    param_data = {
        "stock": {stock_id: "1"},
        "address": "301",
        "stockdetailids": stockdetail_ids,
        "extend": {}
    }
    data = {"param": json.dumps(param_data)}  # 将字典转换为JSON字符串

    # 需要verify=False，不然会报401错误
    r = requests.post(url=url, headers=headers, data=data, verify=False)
    jsessionid_order = basic_analysis_of_response(r)

    return jsessionid_order


def get_yzm_image(session: str, jsessionid: str):
    url = 'http://202.117.17.144/gen'
    headers = {
        'Host': '202.117.17.144',
        'Accept': '*/*',
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0',
        'Referer': 'http://202.117.17.144/yzm/slider.html',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,en-GB;q=0.6',
        'Cookie': f'SESSION={session}; from=undefined; JSESSIONID={jsessionid};'
    }

    import requests
    r = requests.get(url=url, headers=headers, verify=False)
    print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    if r.status_code == 200:
        print("请求成功!")
    else:
        raise Exception("获得验证码图片请求失败!请检查是否在预定时段内（8：40-21：40）。状态码为：" + str(r.status_code))

    import json
    # 将JSON数据解析为Python字典
    data_dict = json.loads(r.text)

    # 提取backgroundImage的值
    background_image_value = str(data_dict['captcha']['backgroundImage']).split(',')[-1]

    # 调用函数，函数返回滑块验证码图片中心缺口的x坐标
    return crack_yzm_image.process_images(background_image_value)


def book(court_id: str, session: str, jsessionid: str, stock_id: str, stockdetail_ids: str, x_index: int, count_try: int):
    import requests

    url = 'http://202.117.17.144/order/book.html'
    headers = {
        'Host': '202.117.17.144',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0',
        'Referer': 'http://202.117.17.144/order/show.html?id=' + str(court_id),
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,en-GB;q=0.6',
        'X-Requested-With': 'XMLHttpRequest',
        'Cookie': f'from=undefined; SESSION={session}; from=undefined; JSESSIONID={jsessionid};'
    }

    param_data = {
        "activityPrice": 0,
        "activityStr": None,
        "address": court_id,
        "dates": None,
        "extend": {},
        "flag": "0",
        "isBulkBooking": None,
        "isbookall": "0",
        "isfreeman": "0",
        "istimes": "0",
        "mercacc": None,
        "merccode": None,
        "order": None,
        "orderfrom": None,
        "remark": None,
        "serviceid": None,
        "shoppingcart": "0",
        "sno": None,
        "stock": {str(stock_id): "1"},
        "stockdetail": {str(stock_id): str(stockdetail_ids)},
        "stockdetailids": str(stockdetail_ids),
        "stockid": None,
        "subscriber": "0",
        "time_detailnames": None,
        "userBean": None,
        "venueReason": None
    }

    yzm_data = crack_yzm_request.bulid_request(x_index=x_index)

    import json
    data = {
        "param": json.dumps(param_data),
        "yzm": json.dumps(yzm_data),
        "json": "true"
    }

    # 需要verify=False，不然会报401错误
    r = requests.post(url=url, headers=headers, data=data, verify=False)
    jsessionid_yzm = basic_analysis_of_response(r)

    # 解析 JSON 数据
    data = json.loads(r.text)

    max_count = 10

    if data['message'] == '验证码有误！':
        print(f'****************验证码有误，系统再次尝试。第{count_try}次输入的验证码为：*******************************')
        print(yzm_data)
        count_try = count_try + 1
        if count_try >= max_count:
            raise Exception(f"已进行{max_count}次尝试，无法通过验证码测试")
        # x_index = x_index + 22  # json文件中显示验证码滑块的大小为66像素。
        import time
        time.sleep(0.5)
        x_index = get_yzm_image(session=session, jsessionid=jsessionid_yzm)
        book(court_id=court_id, stock_id=stock_id, stockdetail_ids=stockdetail_ids,
             x_index=x_index, session=session, jsessionid=jsessionid_yzm, count_try=count_try)
    if data['message'] == '未支付':
        print('预定成功！')
    else:
        print("返回报文出现未知字段：" + data['message'])


def basic_analysis_of_response(r):
    # 获取状态码
    print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    if r.status_code == 200:
        print("请求成功!")
    else:
        raise Exception("请求失败!请检查是否在预定时段内（8：40-21：40）。状态码为：" + str(r.status_code))

    # 获取响应头
    response_headers = r.headers
    print('===========================================================================================================')
    print(response_headers)

    # 获取相应内容
    response_text = r.text
    print('===========================================================================================================')
    print(response_text)

    # 获得变动的jssessionid，进入下一步
    jsessionid = response_headers['Set-Cookie'].split(';')[0].split('=')[-1]
    # 'Set-Cookie': 'JSESSIONID=63014074C416891029BC72FBBADB2552; Path=/; HttpOnly'

    return jsessionid
