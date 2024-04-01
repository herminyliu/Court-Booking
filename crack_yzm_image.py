import base64
from PIL import Image
import io
import numpy as np


def process_images(base64_string):
    decoded_bytes = base64.b64decode(base64_string)
    with open("image.png", "wb") as f:
        f.write(decoded_bytes)
    return change_image_gray(decoded_bytes)


def change_image_gray(img_byte):
    # 读取图片
    image = Image.open(io.BytesIO(img_byte))
    # 获取图片的宽度和高度
    width, height = image.size
    # 创建灰度数组
    binary_array = np.zeros((width, height))
    # 创建灰度图像
    binary_image = Image.fromarray(np.zeros((height, width)), mode='L')  # 这个函数有天坑，array转为image要特别小心！
    # 遍历图片的像素点，将其转换为黑白
    for y in range(height):
        for x in range(width):
            # 获取像素点的颜色
            color = image.getpixel((x, y))
            # 计算灰度值
            gray = int(color[0] * 0.2126 + color[1] * 0.7152 + color[2] * 0.0722)
            # 将像素点的颜色设置为非黑即白
            if gray > 100:
                gray = 255
            else:
                gray = 0
            new_color = gray
            binary_image.putpixel((x, y), new_color)
            binary_array[x, y] = gray
    # 保存黑白图片

    # 找到验证码坐标值
    max_change_count = 0
    x_index = 0
    for w in range(1, width):
        change_count = np.sum((binary_array[w, :] == 0) & (binary_array[w - 1, :] == 255))  # 对于array来说，竖着的反而是长边
        if change_count > max_change_count:
            max_change_count = change_count
            x_index = w
    print("分析得到验证码缺口左侧边线坐标值为：{}".format(x_index))
    import datetime

    # 获取当前时间
    current_time = datetime.datetime.now()

    # 格式化时间为 HHMMSSDDMMYY，保留微秒部分三位小数
    formatted_time = current_time.strftime("%H%M%S.%f")[:-7] + current_time.strftime("%m%y")

    binary_image.save(f"yzm_images/binary_{str(x_index)}_{str(formatted_time)}.jpg", format="JPEG")
    print("验证码黑白二值化图片已保存!")
    return x_index

