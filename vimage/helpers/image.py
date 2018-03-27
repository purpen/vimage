# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from pathlib import *
import random
from enum import Enum, unique
import requests as req
from ..helpers.utils import *
from ..helpers.style import *
from ..helpers.switch import *
from config import *
from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config


@unique
class PosterClass(Enum):
    GoodsInfoWxa = 0    # 商品小程序码
    GoodsSales = 1      # 商品促销


class TextObject:
    """
        文字
    """

    def __init__(self, text_data=None):
        """
        初始化文字对象

        :param text_data: 文字信息
        """

        data = text_data or {}
        style_data = data.get('style') or {}                # 文字样式信息

        self.type = data.get('type')                        # 类型（标题/内容/附加信息等）
        self.content = data.get('content')                  # 内容
        self.position = data.get('position')                # 位置
        self.z_index = data.get('z_index')                  # 层级（文字叠加）
        self.align = style_data.get('align')                # 对齐方式(多行文本)
        self.font_size = style_data.get('font_size')        # 字体大小
        self.font_family = style_data.get('font_family')    # 字体样式
        self.text_color = style_data.get('text_color')      # 文字颜色
        self.line_spacing = style_data.get('line_spacing')  # 行间距(多行文本)


class ImageObject:
    """
        图像
    """

    def __init__(self, image_data=None):
        """
        初始化图片对象

        :param image_data: 图片信息
        """

        data = image_data or {}

        self.type = data.get('type')           # 类型
        self.size = data.get('size')           # 尺寸
        self.position = data.get('position')   # 位置
        self.url = data.get('url')             # url
        self.z_index = data.get('z_index')     # 层级（叠加顺序）


def create_canvas(size, color=(255, 255, 255)):
    """
    创建画布

    :param size: 尺寸
    :param color: 颜色
    :return:
    """

    width = size.get('width')
    height = size.get('height')

    canvas = Image.new('RGBA', (width, height), color)

    return canvas


def draw_line(image, draw_position, color, width=0):
    """
    图片上绘制一条直线

    :param image: 图片
    :param draw_position: 直线的大小、位置 [(x1, y1), (x2, y2)]
    :param color: 颜色
    :param width: 宽度
    :return: 绘制完成的图片
    """

    ImageDraw.Draw(image).line(draw_position, color, width)

    return image


def draw_rectangle(image, draw_position, color):
    """
    图片上绘制矩形

    :param image: 图片
    :param draw_position: 矩形的大小、位置 [(x1, y1), (x2, y2)]
    :param color: 颜色
    :return: 绘制完成的图片
    """

    ImageDraw.Draw(image).rectangle(draw_position, color)

    return image


def image_draw_text(image, text=TextObject()):
    """
    在图片上添加文字

    :param image: 图片
    :param text: 文字
    :return: 画上文字的图片
    """

    # 文字画的位置
    x = text.position.get('x')
    y = text.position.get('y')
    xy = (x, y)

    # 字体的样式
    draw_font = ImageFont.truetype(font=text.font_family,
                                   size=text.font_size)

    # 文字的样式配置
    ImageDraw.Draw(image).text(xy=xy,
                               text=text.content,
                               fill=text.text_color,
                               font=draw_font,
                               align=text.align)

    return image


def load_image_url(image_url):
    """
    加载图片 url

    :return: 图片实例
    """

    # 请求图片链接，生成图片
    r = req.get(image_url)
    image = Image.open(BytesIO(r.content)).convert('RGBA')

    return image


def paste_image(canvas, image_obj=ImageObject()):
    """
    合成图片

    :param canvas: 背景图片
    :param image_obj: 图片素材
    :return: 拼贴后的结果图片
    """

    # 图像的尺寸
    width = image_obj.size.get('width')
    height = image_obj.size.get('height')

    # 图像合成的位置
    x = image_obj.position.get('x')
    y = image_obj.position.get('y')
    xy = (x, y)

    # 对图片合成
    load_image = load_image_url(image_obj.url)

    resize_image = load_image.resize((width, height))
    canvas.paste(resize_image, xy, resize_image)

    return canvas


def image_filename():
    """
    设置图片的文件名

    :return: 文件名
    """

    # 根据时间戳生成文件名
    filename = '%d%d%s' % (int(timestamp()), int(random.random()), '.png')

    return filename


def save_image(image, file_path):
    """
    保存图片

    :param image: 图片
    :param file_path: 文件夹路径
    """

    path = Path(file_path)
    src = ''

    # 判断文件夹是否存在
    if path.exists():
        src = '%s%s%s' % (path, '/', image_filename())
        image.save(fp=src, format='PNG')

    return src


def delete_image(src):
    """
    删除图片

    :param src: 图片路径
    """

    path = Path(src)

    # 判断文件是否存在，删除文件
    if path.exists():
        path.unlink()


def upload_image(src, file_name):
    """
    上传图片到七牛

    :param src: 图片路径
    :param file_name: 文件夹名称
    :return: 上传成功后的图片url
    """

    # 七牛的配置
    q = Auth(Config.QINIU_ACCESS_KEY, Config.QINIU_ACCESS_SECRET)
    bucket_name = Config.QINIU_BUCKET_NAME
    key = '%s%s%s' % (file_name, '/', image_filename())
    token = q.upload_token(bucket_name, key, 3600)

    # 上传图片
    if Path(src).exists() is not True:
        return

    ret, info = put_file(token, key, src)

    # 上传成功后删除静态图片
    delete_image(src)

    # 图片的完整 url
    image_url = '%s%s%s' % (Config.CDN_DOMAIN, '/', ret['key'])

    return image_url


def get_sort_list(original_list, key):
    """
    根据层级关系，对数据排序

    :param original_list: 原数组
    :param key: 根据参数排序
    :return: 排序后的数组
    """

    if len(original_list) > 1:
        sort_list = sorted(original_list, key=lambda e: e.get(key))
        return sort_list

    return original_list


class Poster:
    """
        海报
    """

    def __init__(self, data):
        """
        初始化海报对象

        :param data: 海报展示的信息
        """

        info_data = data or {}

        self.id = info_data.get('id')           # 标识
        self.color = info_data.get('color')     # 颜色
        self.size = info_data.get('size')       # 尺寸
        self.width = self.size.get('width')     # 宽度
        self.height = self.size.get('height')   # 高度
        self.texts = info_data.get('texts')     # 文字
        self.images = info_data.get('images')   # 图片

    def create_poster_image(self):
        """
            创建海报图片
        """

        # 生成画布
        canvas = create_canvas(self.size, self.color)

        # 排序后的图片（图片叠加的顺序）
        image_list = get_sort_list(self.images, 'z_index')

        # 图片素材合成到画布上
        for image_data in image_list:
            image_obj = ImageObject(image_data)
            canvas = paste_image(canvas, image_obj)

        # 排序后的文字（文字叠加的顺序）
        text_list = get_sort_list(self.texts, 'z_index')

        # 文字内容绘制到画布上
        for text_data in text_list:
            text_obj = TextObject(text_data)
            canvas = image_draw_text(canvas, text_obj)

        return canvas


def get_poster_class(poster_class, data, style_id):
    """
    获取海报类型

    :param poster_class: 需要的海报类型
    :param data: 展示的数据
    :param style_id: 海报的样式
    :return:
    """

    poster = None

    for case in Switch(poster_class):
        if case(PosterClass.GoodsInfoWxa):
            poster = GoodsWxaStyle(data, style_id)
            break

        if case(PosterClass.GoodsSales):
            poster = GoodsSalesStyle(data, style_id)
            break

        if case():
            poster = GoodsWxaStyle(data, style_id)

    poster_data = poster.get_style_data()

    return poster_data


def create_poster(data, poster_class, style_id):
    """
    生成海报

    :param data: 海报展示的信息内容
    :param poster_class: 海报类型
    :param style_id: 选择的样式
    :return: 海报图片
    """

    # 商品小程序海报样式数据
    poster_style_data = get_poster_class(poster_class, data, style_id)

    # 生成海报图片
    canvas = Poster(poster_style_data)
    poster_image = canvas.create_poster_image()

    # 保存上传图片
    image_src = save_image(poster_image, 'vimage/resource/test')

    return upload_image(image_src, 'wxa')


