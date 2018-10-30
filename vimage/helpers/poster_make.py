# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
from flask import current_app
from vimage.helpers.qiniu_cloud import QiniuCloud
from vimage.helpers.switch import Switch
from config import *
from vimage.exceptions import *
from vimage.poster_style.poster_style import *
from vimage.helpers.image_tools import load_url_image


class TextObject:
    """
        文字类
    """

    def __init__(self, text_data=None):
        """
        初始化文字对象

        :param text_data: 文字信息
        """

        data = text_data or {}
        style_data = data.get('style', {})                  # 文字样式信息
        self.type = data.get('type')                        # 类型（标题/内容/附加信息等）
        self.content = data.get('content')                  # 内容
        self.position = data.get('position')                # 位置
        self.z_index = data.get('z_index')                  # 层级（文字叠加）
        self.width = data.get('width')                      # 文本在图片中的宽度
        self.align = style_data.get('align')                # 对齐方式(多行文本)
        self.font_size = style_data.get('font_size')        # 字体大小
        self.font_family = style_data.get('font_family')    # 字体样式
        self.text_color = style_data.get('text_color')      # 文字颜色
        self.line_spacing = style_data.get('line_spacing')  # 行间距(多行文本)

    def draw_text(self, canvas):
        """
        绘制文字

        :param canvas: 画布
        :return: 添加文字的图片
        """

        # 字体的样式
        font_path = '%s%s%s' % (current_app.config['MAKE_IMAGE_FONTS_PATH'], self.font_family, '.ttf')
        current_app.logger.debug('Font path: %s' % font_path)
        draw_font = ImageFont.truetype(font=font_path, size=self.font_size)

        # 海报的宽度
        poster_w = canvas.size[0]

        # 文本的尺寸
        text_size = draw_font.getsize(self.content)

        # 重新计算文字内容，保持居中
        if self.align is 'center':
            self.draw_center_text(text_size, poster_w)

        # 是否限定宽度
        if self.width is not None:
            self.draw_cut_content(text_size)

        # 文字的样式配置
        if self.line_spacing is None:
            ImageDraw.Draw(canvas).text(xy=self.position, text=self.content, fill=self.text_color, font=draw_font,
                                        align=self.align)
        else:
            text_spacing = self.line_spacing - self.font_size
            ImageDraw.Draw(canvas).multiline_text(xy=self.position, text=self.content, fill=self.text_color,
                                                  font=draw_font, spacing=text_spacing, align=self.align)

    def draw_center_text(self, text_size, poster_w):
        """
        文字居中

        :param text_size: 绘制文字的尺寸
        :param poster_w: 海报的宽度
        :return: 文本刷新位置
        """

        if text_size[0] < poster_w:
            position_x = (poster_w - text_size[0]) / 2
            self.position = (position_x, self.position[1])
            return self.position

        return self.position

    def draw_cut_content(self, text_size):
        """
        根据限定宽度，切割内容文本

        :param text_size: 绘制文字的尺寸
        :return 格式化后的文字
        """

        if text_size[0] > self.width:
            text_w = text_size[0] / len(self.content)  # 单个字符的宽度
            line_text_count = int(self.width / text_w)  # 每排显示字符数量
            line_count = int(len(self.content) / line_text_count) + 1  # 行数

            content_text = ''
            for i in range(line_count):
                start_index = line_text_count * i  # 截取的文字起始位置
                line_text = self.content[start_index: line_text_count + start_index] + '\n'  # 每行的文字，末尾添加换行
                content_text += line_text  # 结果拼接的文字

            # 最终的内容文字
            self.content = content_text.strip()

            # 格式化过长的内容
            self.format_more_text(line_text_count, line_count)

        return self.content

    def format_more_text(self, text_count, line_count):
        """
        格式化过长的文字，末尾添加'...'

        :param text_count: 显示文字数量
        :param line_count: 总行数
        :return: 格式化后的文字
        """

        # 最后一行文字的长度
        end_text_len = len(self.content) - text_count * int(line_count - 2)

        if end_text_len > text_count:
            self.content = self.content[:len(self.content) - 1] + '...'

        return self.content


class ImageObject:
    """
        图像类
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
        self.radius = data.get('radius')       # 圆角半径
        self.url = data.get('url')             # 网络Url
        self.path = data.get('path')           # 本地图片路径
        self.z_index = data.get('z_index')     # 层级（叠加顺序）

    def paste_image(self, canvas):
        """
        粘贴图片

        :param canvas: 画布
        :return: 拼贴后的结果图片
        """

        # 加载图片
        if self.url is None:
            load_image = load_static_image(self.path)
        else:
            load_image = load_url_image(self.url, is_create=True)

        result_image = self.square_image(load_image)
        result_image = crop_image(result_image, self.size)

        # 圆角半径
        if self.radius > 0:
            result_image = circular_bead_image(result_image, self.radius)

        # 对图片合成
        canvas.paste(result_image, self.position, result_image)

    def square_image(self, image):
        """
            原图裁剪为正方形
        """

        square_image_type_list = [ImageType.Goods, ImageType.Avatar, ImageType.BrandLogo,
                                  ImageType.WxaCode, ImageType.QRCode]

        if self.type in square_image_type_list:
            image = square_image(image)

        return image


class ShapeObject:
    """
        图形类
    """

    def __init__(self, shape_data=None):
        """
        初始化图形对象

        :param shape_data: 图形样式信息
        """

        data = shape_data or {}

        self.type = data.get('type')            # 类型
        self.position = data.get('position')    # 位置
        self.width = data.get('width')          # 宽度
        self.color = data.get('color')          # 填充颜色
        self.out_color = data.get('out_color')  # 边框颜色
        self.z_index = data.get('z_index')      # 层级（叠加顺序）

    def draw_line(self, image):
        """
        图片上绘制一条直线

        :param image: 图片
        :return: 绘制完成的图片
        """

        ImageDraw.Draw(image).line(self.position, self.color, self.width)

    def draw_rectangle(self, image):
        """
        图片上绘制矩形

        :param image: 图片
        :return: 绘制完成的图片
        """

        ImageDraw.Draw(image).rectangle(self.position, self.color, self.out_color)

    def draw_circle(self, image):
        """
        图片上绘制圆形

        :param image: 图片
        :return: 绘制完成的图片
        """

        ImageDraw.Draw(image).ellipse(self.position, self.color, self.out_color)

    def draw_shapes(self, canvas):
        """
        在图片上绘制图形

        :param canvas: 画布
        :return: 绘制完成的图片
        """

        shape_type = self.type

        for case in Switch(shape_type):
            if case(DrawShapeType.Line):
                self.draw_line(canvas)
                break

            if case(DrawShapeType.Rectangle):
                self.draw_rectangle(canvas)
                break

            if case(DrawShapeType.Circle):
                self.draw_circle(canvas)
                break


def create_canvas(size, color=(255, 255, 255), mode='RGBA'):
    """
    创建画布

    :param mode: 模式
    :param size: 尺寸
    :param color: 颜色
    :return: image
    """

    canvas = Image.new(mode, size, color)

    return canvas


class Poster(object):
    """
        海报生成器
    """

    def __init__(self, post_data):
        """
        初始化海报对象

        :param post_data: 海报展示的信息
        """

        self.data = post_data or {}

        self.id = self.data.get('id')  # 样式标识
        self.color = self.data.get('color')  # 背景颜色
        self.size = self.data.get('size')  # 尺寸
        self.views = self.data.get('views')  # 视图

        # 创建初始画布
        self.canvas = create_canvas(self.size, self.color)

    def create_container_view(self, style_data):
        """
            制作容器视图
        """

        size = style_data.get('size')
        images = style_data.get('images')
        texts = style_data.get('texts')
        shapes = style_data.get('shapes')

        # 容器视图
        container_canvas = create_canvas(size=size, color=self.color)

        # 1:绘制图形（分割线，文字背景色等）
        shape_list = _sort_list_layer(shapes, 'z_index')
        for shape_data in shape_list:
            ShapeObject(shape_data).draw_shapes(container_canvas)

        # 2:图片素材合成到画布上
        image_list = _sort_list_layer(images, 'z_index')
        for image_data in image_list:
            ImageObject(image_data).paste_image(container_canvas)

        # 3:文字内容绘制到画布上
        text_list = _sort_list_layer(texts, 'z_index')
        for text_data in text_list:
            TextObject(text_data).draw_text(container_canvas)

        return container_canvas

    def make_goods_card(self):
        """
            制作商品分享卡片
        """

        # 顶部间隔
        view_h = 0

        # 合并所有的视图容器
        for item in self.views:
            view_canvas = self.create_container_view(item)
            self.canvas.paste(view_canvas, (0, view_h), view_canvas)
            view_h += item.get('size')[1]

        return self.canvas

    def make_poster_card(self):
        """
            生成海报
        """

        # 海报画布
        poster_canvas = self.create_container_view(self.data)

        return poster_canvas


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
