# 按间距中的绿色按钮以运行脚本。
import send_request
import time

if __name__ == '__main__':
    # 11点29分：目前先做一个订单订一个场的，多个场的POST报文的请求体需要改
    # 如果场子已经被订了怎么办？？？
    # 如果不在预定时段booking_tennis.findtime会直接返回404
    start_time = time.time()
    my_session = '07a7c653-1f07-47b9-83e5-f3d754c710fb'  # 一段时间之内不会变
    my_book_date = '2024-03-29'  # 注意，提供的场地日期时间一定要有效
    my_time_no = '08:00-09:00'  # 注意，提供的场地日期时间一定要有效
    # 下午14点到15点应写成14：01-15：00
    # 上午8点到9点应写成08:00-09:00
    my_court_id = '301'  # 301代表东南网球场
    court_num: int = 0  # 代表预定一号场

    jsessionid_findtime, my_stock_id = send_request.findtime(court_id=my_court_id,
                                                    book_date=my_book_date, time_no=my_time_no, session=my_session)
    # findtime函数获得了stock_id

    jsessionid_findprice = send_request.findprice(court_id=my_court_id, book_date=my_book_date, time_no=my_time_no,
                  session=my_session, jsessionid=jsessionid_findtime)

    jsessionid_findseat, my_stock_detailid = send_request.findseat(court_id=my_court_id, stock_id=my_stock_id,
                 session=my_session, jsessionid=jsessionid_findprice, court_num=court_num)
    # findseat函数获得了stock_detailid

    jsessionid_order = send_request.order(court_id=my_court_id, stock_id=my_stock_id, stockdetail_ids=my_stock_detailid,
                                 session=my_session, jsessionid=jsessionid_findseat)

    x_index = send_request.get_yzm_image(session=my_session, jsessionid=jsessionid_order)

    send_request.book(court_id=my_court_id, stock_id=my_stock_id, stockdetail_ids=my_stock_detailid, x_index=x_index,
                        session=my_session, jsessionid=jsessionid_order, count_try=0)

    end_time = time.time()

    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(
        f"预定成功！场地信息为：\n日期：{my_book_date}  时段：{my_time_no}  场地编号：{court_num + 1}号场\n请尽快手动支付！")
    print(f"程序运行时间{end_time - start_time}秒")

