import datetime
import random

# 获取当前 UTC 时间
utc_now = datetime.datetime.utcnow()
print(utc_now)

# 生成服从正态分布的随机微小量，均值为 50 毫秒，方差为 20 毫秒
delayed_milliseconds = random.normalvariate(50, 20)

# 将微小量保留到三位小数
delayed_milliseconds = round(delayed_milliseconds, 3)

# 将微小量转换为 timedelta 对象
delayed_timedelta = datetime.timedelta(milliseconds=delayed_milliseconds)

# 计算加上微小量后的时间
delayed_utc_time = utc_now + delayed_timedelta

# 将时间格式化为指定的字符串形式
iso_format = delayed_utc_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

print("加上微小量后的 UTC 时间：", iso_format)
