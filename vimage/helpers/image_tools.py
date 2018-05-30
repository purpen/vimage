# -*- coding:utf-8 -*-
import requests as req
from PIL import Image, ImageDraw
from io import BytesIO
import imagehash

from vimage.constant import *
from vimage.helpers.utils import *


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


def image_hash(image, hash_size=8):
    """
    图片的 hash 处理

    :param image: 图片对象
    :param hash_size: 尺寸，默认 =8
    :return: hash 值
    """

    hash = imagehash.dhash(image, hash_size=hash_size)

    return hash


def hamming(hash1, hash2):
    """
    相似度计算：汉明距离

    :param hash1: 图片的指纹 1
    :param hash2: 图片的指纹 2
    :return: 相似度，越大越相似
    """

    result = 1 - (hash1 - hash2) / len(hash1.hash) ** 2

    return result


def similar_images(input_image_url, data_image_urls):
    """
    相似图片比对

    :param input_image_url: 输入图片 url
    :param data_image_urls: 数据图片集 url
    :return: 比对结果
    """

    # 加载输入的图片，进行 hash
    input_img = load_url_image(input_image_url)
    input_img_hash = image_hash(input_img, hash_size=8)

    # 加载图片数据集，计算图片的相似度
    result = []
    for data_img_url in data_image_urls:
        data_img_hash = image_hash(load_url_image(data_img_url), hash_size=8)
        hamming_len = hamming(input_img_hash, data_img_hash)

        # 保存相似度结果
        result.append({'img_url': data_img_url,
                       'similarity': hamming_len})

        # 进行升降排序
        if len(result) > 1:
            result = sorted(result, key=lambda e: e.get('similarity'))
            result.reverse()

    return {
        'original_img': input_image_url,
        'result': result
    }