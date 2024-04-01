def bulid_request(x_index: int):
    # 伪造验证码报文，个人认为startSlidingTime，entSlidingTime服务器应该没管，因为3-22号下午曾使用3-19号的startSlidingTime成功预定

    startSlidingTime, endSlidingTime = startEndSlidingTime(x_index=x_index)
    # bgImageWidth bgImageHeight sliderImageWidth sliderImageHeight 均为定值
    unkonwn_string = "22a831d54f814f9ba8699f0d407ca995"
    yzm_data = {
        "bgImageWidth": 260,
        "bgImageHeight": 0,
        "sliderImageWidth": 0,
        "sliderImageHeight": 159,
        "startSlidingTime": str(startSlidingTime),
        "entSlidingTime": str(endSlidingTime),
        "trackList": "[{'x': 0, 'y': 0, 'type': 'down', 't': 68},"
                     " {'x': 10, 'y': 0, 'type': 'move', 't': 81},"
    }
    # generate_mouse_movement_tracklist(x_index)
    yzm_data = str(yzm_data) + f"synjones{unkonwn_string}synjoneshttp://202.117.17.144:8071 "
    return yzm_data


def startEndSlidingTime(x_index: int):
    from datetime import datetime, timedelta
    import random

    # 获取当前的 UTC 时间
    utc_now = datetime.utcnow()

    # 生成服从正态分布的随机毫秒数，均值为50毫秒，方差为20毫秒
    random_delay = random.gauss(50, 20)

    # 将随机毫秒数添加到当前 UTC 时间中
    delayed_utc_time = utc_now + timedelta(milliseconds=random_delay) + timedelta(milliseconds=-3500)

    # 将结果格式化为 ISO 8601 格式的字符串，并且根据格式，只保留三位小数
    startSlidingTime = delayed_utc_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

    # 生成startSlidingTime和endSlidingTime之间的间隔，根据之前的观察，取均值为1.5s，方差为0.3s
    random_slidingtime = random.gauss(200, 30) + int(x_index) * 1.8

    endSlidingTime = utc_now + timedelta(milliseconds=random_slidingtime) + timedelta(milliseconds=-3500)

    endSlidingTime = endSlidingTime.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

    return startSlidingTime, endSlidingTime


def generate_mouse_movement_tracklist(x_index: int):
    import json
    import random
    from datetime import datetime, timedelta

    track_list = []

    # 生成鼠标移动记录
    x = 0
    y = 0
    t = 68
    missing_square = 66
    x_goal = round((x_index + missing_square/2) * 278 / 590)  # 从渲染验证码框的js文件可以读出，虽然图片像素一般为590，但放置图片的验证码框仅为278像素，需要缩小
    print(f"根据验证码窗体修正后距离:{x_goal}")
    track_list.append({"x": x, "y": y, "type": "down", "t": t})
    for _ in range(100):
        # 添加一个随机变化到x值
        x += random.normalvariate(10, 1)
        x = round(x)
        if x > x_goal:
            break
        # 随机调整y值
        y += random.choices([0, 1, -1], weights=[0.8, 0.1, 0.1])[0]
        y = max(-1, min(y, 1))  # 确保y保持在范围内
        y = round(y)
        # 根据均值为18，方差为3的正态分布生成时间间隔
        t += int(random.normalvariate(18, 2.5))
        t = round(t)
        track_list.append({"x": x, "y": y, "type": "move", "t": t})

    track_list.append({"x": str(x_goal), "y": str(0), "type": "up", "t": str(t + 18)})

    return track_list  # json.dump不能放在这里

