# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
from flask import current_app
from vimage.helpers.qiniu_cloud import QiniuCloud
from config import *


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

        self.url = data.get('url')             # 网络Url

        self.z_index = data.get('z_index')     # 层级（叠加顺序）


class Poster(object):
    """
        海报生成器
    """

    # 默认颜色
    default_color = (255, 255, 255)

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

        # 创建初始画布
        self.canvas = self.create_canvas()

    def create_canvas(self):
        """创建画布"""
        return Image.new('RGBA', (self.width, self.height), self.color)

    def draw_text(self, text=TextObject()):
        """
        在图片上添加文字

        :param text: 文字
        :return: 画上文字的图片
        """

        # 文字画的位置
        x = text.position.get('x')
        y = text.position.get('y')
        xy = (x, y)

        # 字体的样式
        font_path = '%s%s%s' % (current_app.config['MAKE_IMAGE_FONTS_PATH'], text.font_family, '.ttf')
        current_app.logger.debug('Font path: %s' % font_path)
        draw_font = ImageFont.truetype(font=font_path,
                                       size=text.font_size)

        # 文字的样式配置
        ImageDraw.Draw(self.canvas).text(xy=xy, text=text.content, fill=text.text_color, font=draw_font,
                                         align=text.align)

    def draw_line(self, draw_position, color, width=0):
        """
        图片上绘制一条直线

        :param draw_position: 直线的大小、位置 [(x1, y1), (x2, y2)]
        :param color: 颜色
        :param width: 宽度
        :return: 绘制完成的图片
        """

        ImageDraw.Draw(self.canvas).line(draw_position, color, width)

    def draw_rectangle(self, draw_position, color):
        """
        图片上绘制矩形

        :param draw_position: 矩形的大小、位置 [(x1, y1), (x2, y2)]
        :param color: 颜色
        :return: 绘制完成的图片
        """

        ImageDraw.Draw(self.canvas).rectangle(draw_position, color)

    def paste_image(self, image_obj=ImageObject()):
        """
        合成图片

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

        # 加载图片
        load_image = QiniuCloud.load_image(image_obj.url)
        resize_image = load_image.resize((width, height))

        # 对图片合成
        self.canvas.paste(resize_image, xy, resize_image)

    def make(self):
        """开始生成海报"""

        # 1、排序后的图片（图片叠加的顺序）
        image_list = _sort_list_layer(self.images, 'z_index')

        # 2、图片素材合成到画布上
        for image_data in image_list:
            image_obj = ImageObject(image_data)
            self.paste_image(image_obj)

        # 3、排序后的文字（文字叠加的顺序）
        text_list = _sort_list_layer(self.texts, 'z_index')

        # 4、文字内容绘制到画布上
        for text_data in text_list:
            text_obj = TextObject(text_data)
            self.draw_text(text_obj)

        return self.canvas


def _sort_list_layer(original_list, key):
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
