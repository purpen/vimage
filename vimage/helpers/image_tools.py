# -*- coding:utf-8 -*-
from io import BytesIO
import requests as req
from PIL import Image, ImageDraw
from vimage.helpers.utils import *
from vimage.constant import *


def load_url_image(image_url, is_create=False):
    """
    通过 url 加载图片

    :param image_url: 图片链接
    :param is_create: 链接获取失败时是否创建图片
    :return:
    """

    # 默认创建的图片
    image = Image.new('RGBA', Size.DEFAULT_IMAGE_SIZE['square'], Colors.DEFAULT_BACKGROUND_COLOR['white']).copy()

    # 图片链接是否存在
    if not image_url:
        return image if is_create else custom_response('图片链接不存在', 400, False)

    # 请求图片链接，生成图片
    try:
        r = req.get(image_url)
        image = Image.open(BytesIO(r.content)).copy().convert('RGBA')

    except (req.exceptions.HTTPError, req.exceptions.URLRequired):
        return image if is_create else custom_response('图片链接获取失败', 400, False)

    return image


def linear_colour(color_1, color_2, t):
    """
    混合颜色

    :param color_1: 颜色1
    :param color_2: 颜色2
    :param t:
    :return:
    """

    r = int(color_1[0] + (color_2[0] - color_1[0]) * t)
    g = int(color_1[1] + (color_2[1] - color_1[1]) * t)
    b = int(color_1[2] + (color_2[2] - color_1[2]) * t)

    return r, g, b


def gradient_color(color1=(255, 255, 255), color2=(0, 0, 0), w=256, h=256, direction=0):
    """
    创建渐变色图片

    :param color1: 颜色1
    :param color2: 颜色2
    :param w: 宽度
    :param h: 高度
    :param direction: 渐变的方向，0:上下 / 1:左右，默认为0
    :return: 渐变色图片
    """

    # 颜色列表
    list_of_colors = [color1, color2]

    no_steps = h

    # 梯度颜色
    gradient = []

    for i in range(len(list_of_colors) - 1):
        for j in range(no_steps):
            gradient.append(linear_colour(list_of_colors[i],
                                          list_of_colors[i + 1],
                                          j / no_steps))

    # 初始化图片
    color_img = Image.new("RGB", (w, h))

    # 填充像素颜色
    for x in list(range(w)):
        for y in list(range(h)):
            xy = (x, y) if direction == 0 else (y, x)
            color_img.putpixel(xy, gradient[y])

    return color_img


def circle_image(image):
    """
    裁剪圆形图像

    :param image: 图片
    :return: 裁圆后的图片
    """

    image = image.convert("RGBA")
    size = image.size
    r2 = min(size[0], size[1])

    if size[0] != size[1]:
        image = image.resize((r2, r2), Image.ANTIALIAS)

    circle = Image.new('L', (r2, r2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, r2, r2), fill=255)
    alpha = Image.new('L', (r2, r2), 255)
    alpha.paste(circle, (0, 0))
    image.putalpha(alpha)

    return image
