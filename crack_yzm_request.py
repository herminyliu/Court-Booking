def bulid_request(x_index: int):
    # 伪造验证码报文，个人认为startSlidingTime，entSlidingTime服务器应该没管，因为3-22号下午曾使用3-19号的startSlidingTime成功预定
    # bgImageWidth bgImageHeight sliderImageWidth sliderImageHeight 均为定值
    unkonwn_string = "22a831d54f814f9ba8699f0d407ca995"
    track_list, startSlidingTime, endSlidingTime= generate_mouse_movement_tracklist(x_index=x_index)
    yzm_data = {
        "bgImageWidth": 260,
        "bgImageHeight": 0,
        "sliderImageWidth": 0,
        "sliderImageHeight": 159,
        "startSlidingTime": str(startSlidingTime),
        "entSlidingTime": str(endSlidingTime),
        "trackList": track_list
    }
    # generate_mouse_movement_tracklist(x_index)
    yzm_data = str(yzm_data) + f"synjones{unkonwn_string}synjoneshttp://202.117.17.144:8071 "
    return yzm_data


def generate_mouse_movement_tracklist(x_index: int):
    import json
    import random
    from datetime import datetime, timedelta
    utc_now = datetime.utcnow()
    startSlidingTime = utc_now.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    track_list = []

    # 生成鼠标移动记录
    x = 0
    y = 0
    t_start: int = random.normalvariate(100, 20)
    t = t_start
    t_goal: int = random.normalvariate(700, 100)
    x_goal: int = round(x_index / 2.4)  # 从渲染验证码框的js文件可以读出，虽然图片像素一般为590，但放置图片的验证码框仅为278像素，需要缩小
    print(f"根据验证码窗体修正后距离:{x_goal}")
    track_list.append({"x": x, "y": y, "type": "down", "t": round(t_start)})
    for _ in range(round((t_goal - t_start) / 32)):
        # 添加一个随机变化到x值
        x += random.normalvariate(10, 1)
        x = round(x)

        y = 0  # 手稳，一直为0哈哈哈
        # 根据均值为18，方差为3的正态分布生成时间间隔
        t = round(t + random.normalvariate(32, 5))
        if x > x_goal or t > t_goal:
            break
        track_list.append({"x": x, "y": y, "type": "move", "t": t})

    track_list.append({"x": str(x_goal), "y": 0, "type": "up", "t": round(t_goal)})
    endSlidingTime = utc_now + timedelta(milliseconds=t_goal * (-1)) + timedelta(milliseconds=random.normalvariate(50, 10))
    endSlidingTime = endSlidingTime.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

    return track_list, startSlidingTime, endSlidingTime  # json.dump不能放在这里


# def startEndSlidingTime(x_index: int):
#     import random
#
#     # 获取当前的 UTC 时间
#     utc_now = datetime.utcnow()
#
#     # 生成服从正态分布的随机毫秒数，均值为50毫秒，方差为20毫秒
#     random_delay = random.gauss(50, 20)
#
#     # 将随机毫秒数添加到当前 UTC 时间中
#     delayed_utc_time = utc_now + timedelta(milliseconds=random_delay) + timedelta(milliseconds=-3500)
#
#     # 将结果格式化为 ISO 8601 格式的字符串，并且根据格式，只保留三位小数
#     startSlidingTime = delayed_utc_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
#
#     # 生成startSlidingTime和endSlidingTime之间的间隔，根据之前的观察，取均值为1.5s，方差为0.3s
#     random_slidingtime = random.gauss(200, 30) + int(x_index) * 1.8
#
#     endSlidingTime = utc_now + timedelta(milliseconds=random_slidingtime) + timedelta(milliseconds=-3500)
#
#     endSlidingTime = endSlidingTime.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
#
#     return startSlidingTime, endSlidingTime
