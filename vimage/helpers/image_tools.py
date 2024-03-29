# -*- coding:utf-8 -*-
import requests as req
import imagehash
import random
import re
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from pathlib import Path
from vimage.constant import *
from vimage.helpers.utils import *
from flask import current_app


def get_text_width(text, font_size, font_family=None):
    """
    获取文字的宽度

    :param text: 文字
    :param font_size: 字符大小
    :param font_family: 字体样式
    :return: 内容宽度
    """

    # 字体名称
    font_name = font_family if font_family is not None else Fonts.DEFAULT_FONT_FAMILY
    font_path = '%s%s%s' % (current_app.config['MAKE_IMAGE_FONTS_PATH'], font_name, '.ttf')
    draw_font = ImageFont.truetype(font=font_path, size=font_size)

    # 文本的尺寸
    text_size = draw_font.getsize(text)

    return int(text_size[0])


def get_text_count(text, font_size, fixed_width, font_family=None):
    """
    固定宽度可显示的文字数量

    :param text: 文字内容
    :param font_size: 字符大小
    :param fixed_width: 固定宽度
    :param font_family: 字体样式
    :return: 文字数量
    """

    if text is None:
        return 0

    # 字体名称
    font_name = font_family if font_family is not None else Fonts.DEFAULT_FONT_FAMILY
    font_path = '%s%s%s' % (current_app.config['MAKE_IMAGE_FONTS_PATH'], font_name, '.ttf')
    draw_font = ImageFont.truetype(font=font_path, size=font_size)

    # 内容的宽度
    text_width = int(draw_font.getsize(text)[0])

    # 单个文字占的宽度
    single_text_w = int(text_width / len(text))

    # 固定宽度可显示的数量
    text_count = int(fixed_width / single_text_w)

    return text_count


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


def load_static_image(image_path):
    """
    加载本地图片

    :param image_path: 路径
    :return: 图片
    """

    if image_path is not None:
        if Path(image_path).exists():
            return Image.open(image_path).copy().convert('RGBA')

    return Image.new('RGBA', Size.DEFAULT_IMAGE_SIZE['square'], Colors.DEFAULT_BACKGROUND_COLOR['white']).copy()


def hex_to_rgb(hex_color):
    """
        HEX 色值转换成 RGB
    """

    opt = re.findall(r'(.{2})', hex_color[1:] if hex_color[0] is '#' else hex_color)

    rgb = []
    for i in range(0, len(opt)):
        rgb.append(int(opt[i], 16))

    return rgb


def rgb_to_hex(rgb_color):
    """
        RGB 色值转换成 HEX
    """

    rgb = rgb_color.split(",")
    hex = "#"

    for i in range(0, len(rgb)):
        num = int(rgb[i])

        # 每次转换之后只取0x7b的后两位，拼接到 hex
        hex += hex(num)[-2:]

    print("转换后的16进制值为：", hex)
    return hex


def random_color():
    """
        生成随机的颜色
    """
    # 随机的颜色
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    color = (r, g, b)

    return color


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

    result_image = image.convert("RGBA")

    if image.size[0] > image.size[1]:
        result_image = image.crop([0, 0, image.size[1], image.size[1]])

    elif image.size[0] < image.size[1]:
        result_image = image.crop([0, 0, image.size[0], image.size[0]])

    size = result_image.size
    r2 = min(size[0], size[1])

    if size[0] != size[1]:
        result_image = result_image.resize((r2, r2), Image.ANTIALIAS)

    circle = Image.new('L', (r2, r2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, r2, r2), fill=255)
    alpha = Image.new('L', (r2, r2), 255)
    alpha.paste(circle, (0, 0))

    result_image.putalpha(alpha)

    return result_image


def square_image(image):
    """
    裁剪成正方形

    :param image: 图片
    :return: 裁圆后的图片
    """

    result_image = image.convert("RGBA")

    if image.size[0] > image.size[1]:
        # (左、上、右、下)
        crop_left = (image.size[0] - image.size[1]) / 2
        crop_w = image.size[0] - crop_left
        result_image = image.crop([int(crop_left), 0, int(crop_w), image.size[1]])

    elif image.size[0] < image.size[1]:
        crop_top = (image.size[1] - image.size[0]) / 2
        crop_h = image.size[1] - crop_top
        result_image = image.crop([0, crop_top, image.size[0], crop_h])

    else:
        pass

    return result_image


def crop_image(image, size):
    """
    裁剪图片，防止变形

    :param image: 图片
    :param size: 设定尺寸
    :return: 裁剪图片
    """

    if size[0] >= size[1]:
        new_image_h = image.size[1] * (size[0] / image.size[0])
        image = image.resize((int(size[0]), int(new_image_h)), Image.ANTIALIAS)

    elif size[0] < size[1]:
        new_image_w = image.size[0] * (size[1] / image.size[1])
        image = image.resize((int(new_image_w), int(size[1])), Image.ANTIALIAS)

    if image.size[0] > size[0]:
        image_scale_w = (image.size[1] / size[1]) * size[0]
        crop_w = image.size[0] - image_scale_w

        # (左、上、右、下)
        image = image.crop([0, 0, image.size[0] - crop_w, image.size[1]])

    if image.size[1] > size[1]:
        crop_h = image.size[1] - size[1]
        image = image.crop([0, 0, image.size[0], image.size[1] - crop_h])

    return image


def circular_bead_image(image, radius):
    """
    图像添加圆角

    :param image: 图片
    :param radius: 半径
    :return: 图片结果
    """

    circle = Image.new('L', (radius * 2, radius * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, radius * 2, radius * 2), fill=255)
    alpha = Image.new('L', image.size, 255)

    w, h = image.size

    alpha.paste(circle.crop((0, 0, radius, radius)), (0, 0))
    alpha.paste(circle.crop((0, radius, radius, radius * 2)), (0, h - radius))
    alpha.paste(circle.crop((radius, 0, radius * 2, radius)), (w - radius, 0))
    alpha.paste(circle.crop((radius, radius, radius * 2, radius * 2)), (w - radius, h - radius))

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


def noisy_image(image_url, alpha=0.65, default_size=(300, 300)):
    """
    图片添加噪点

    :param image_url: 背景图片url
    :param alpha: 透明度
    :param default_size: 默认尺寸
    :return: 结果图片
    """

    main_image = load_url_image(image_url).resize(default_size).convert('RGBA')

    # 获取图片的尺寸
    w, h = main_image.size

    # 初始化图片
    noisy_img = Image.new("RGBA", (w, h))

    # 填充像素颜色
    for x in list(range(w)):
        for y in list(range(h)):
            xy = (x, y)
            noisy_img.putpixel(xy, random_color())

    main_image = Image.blend(noisy_img, main_image, 1 - alpha)

    return main_image