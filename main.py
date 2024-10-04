# 按间距中的绿色按钮以运行脚本。
import send_request
import time
import argparse

argp = argparse.ArgumentParser(description='Booking court in Xi\'an Jiaotong University')
argp.add_argument('--court_name', help="Choose Which kind of court user is going to book in CHINESE", type=str)
argp.add_argument('--session_id', help="session_id used for logging in", type=str)
argp.add_argument('--book_date', help="date user is going to book, must be valid value in th form YYYY-MM-DD", type=str)
argp.add_argument('--book_time', help="time user is going to book, must be valid value in th form HH:00-HH:00",
                  type=str)
argp.add_argument('--court_id', help="court_id the user is going to book, must be in the valid range", default=0,
                  type=int)  # 默认预定一号场
args = argp.parse_args()

"""
这是针对西安交通大学的体育场地预定程序，给定需要预定的场地类别、日期、时段、场地编号后，即可递归预定，一次只能预定一小时
如果需要连续预定两小时，那么运行程序两遍(即并发调用run.sh两次，或更改run.sh内的内容)
"""

def one_try(court_name, book_date, time_no, session, court_num):
    # 命名并不连贯，这里的court_name在send_requests中其实是court_id！
    jsessionid_findtime = send_request.findtime(court_id=court_name, book_date=book_date, time_no=time_no,
                                                          session=session, court_num=court_num)
    # findtime函数返回的报文中含有stock_id，但只是预定日期当天第一个时段的stock_id

    jsessionid_findprice, stock_id= send_request.findprice(court_id=court_name, book_date=book_date, time_no=time_no,
                                                  session=session, jsessionid=jsessionid_findtime)
    # findprice函数返回的报文中含有stock_id，并且预定日期当天指定时段的stock_id，为所有同场地类型、同日期、同时段的所有场地共享

    jsessionid_findseat, stock_detailid = send_request.findseat(court_id=court_name, stock_id=stock_id,
                                                                session=session, jsessionid=jsessionid_findprice,
                                                                court_num=court_id)
    # findseat函数获得了stock_detailid，精确到具体场地类型、日期、时段、场地编号。

    jsessionid_order = send_request.order(court_id=court_name, stock_id=stock_id,
                                          stockdetail_ids=stock_detailid,
                                          session=session, jsessionid=jsessionid_findseat)

    x_index = send_request.get_yzm_image(session=session, jsessionid=jsessionid_order)

    send_request.book(court_id=court_name, stock_id=stock_id, stockdetail_ids=stock_detailid, x_index=x_index,
                      session=session, jsessionid=jsessionid_order, count_try=0)


def validate_time_format(time_string):
    import re
    # 定义正则表达式，确保格式为 HH:MM-HH:MM，且没有空格
    pattern = r"^\d{2}:\d{2}-\d{2}:\d{2}$"

    # 先验证基本的格式
    if not re.match(pattern, time_string):
        return False

    # 将时间字符串分为开始时间和结束时间
    start_time, end_time = time_string.split('-')

    # 提取小时和分钟
    start_hour, start_minute = map(int, start_time.split(':'))
    end_hour, end_minute = map(int, end_time.split(':'))

    # 验证小时和分钟是否在合理的范围内
    if not (0 <= start_hour < 24 and 0 <= end_hour < 24):
        return False
    if not (0 <= start_minute < 60 and 0 <= end_minute < 60):
        return False
    return True


if __name__ == '__main__':
    # 11点29分：目前先做一个订单订一个场的，多个场的POST报文的请求体需要改
    # 如果场子已经被订了怎么办？？？
    # 如果不在预定时段booking_tennis.findtime会直接返回404
    assert args.session_id is not None
    assert args.book_date is not None
    assert validate_time_format(args.book_time) is True
    assert args.court_name is not None
    assert 1 <= args.court_id <= 20  # 场地编号从1开始
    start_time = time.time()
    my_session = args.session_id  # 一段时间之内不会变
    my_book_date = args.book_date  # 注意，提供的场地日期时间一定要有效
    my_time_no = args.book_time  # 注意，提供的场地日期时间一定要有效
    # 下午14点到15点应写成14：01-15：00
    # 上午8点到9点应写成08:00-09:00
    # 上午9点到10点应写成09:01-10:00
    court_id_table = {"东南网球场": '301', "文体中心三楼羽毛球场地": '42', "文体中心一楼羽毛球场地": '41'}
    my_court_name = court_id_table[args.court_name]  # 301代表东南网球场
    court_id = args.court_id  # 代表预定一号场，在sending_request中court_id代表场地类型，这里代表几号场地。


    def try_booking(try_court_id):
        try:
            one_try(my_court_name, my_book_date, my_time_no, my_session, try_court_id)
            end_time = time.time()

            print("*" * 80)
            print(
                f"预定成功！场地信息为：\n日期：{my_book_date}  时段：{my_time_no}  场地编号：{try_court_id + 1}号场\n请尽快手动支付！")
            print(f"程序运行时间{end_time - start_time}秒")
            exit(0)
        except AssertionError:
            print('*'*25 + '已被抢订/被预订，搜寻剩余可用场地' + '*'*25)
            try_court_id, status = send_request.search_remaining_court()  # 获得用户需要的日期时段剩余的场次编号中的第一个
            if status:
                try_booking(try_court_id)
            else:
                print('*'*25 + '所有场地均被预定完，程序结束' + '*'*25)
                exit(1)

    try_booking(court_id)
