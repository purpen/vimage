# -*- coding: utf-8 -*-
from enum import Enum, unique
from ..helpers import switch, sensitive
from ..constant import *

@unique
class ImageType(Enum):
    Goods = 0           # 商品图
    Background = 1      # 背景
    QRCode = 2          # 二维码
    Logo = 3            # logo
    BrandIcon = 4       # 品牌头像
    Border = 5          # 边框
    Modify = 6          # 修饰
    Mask = 7            # 蒙版


@unique
class TextType(Enum):
    Title = 0       # 标题
    SalePrice = 1   # 价格
    Hint = 2        # 提示
    BrandName = 3   # 品牌名称
    Info = 4        # 其他信息
    Time = 5        # 时间
    SalesTitle = 6  # 促销标题
    SalesInfo = 7   # 促销信息
    SalesPCT = 8    # 促销百分比
    SalesBrand = 9  # 促销品牌


def get_text_content(text_type, data):
    """
    根据类型获取对应的文字内容

    :param text_type: 文字类型
    :param data: 文字数据
    :return: 文字内容
    """

    content = ''

    for case in switch.Switch(text_type):
        if case(TextType.Title):
            content = data.get('title')
            break

        if case(TextType.SalePrice):
            content = '￥%s' % data.get('sale_price')
            break

        if case(TextType.Hint):
            content = data.get('hint_text') or '长按识别小程序码访问'
            break

        if case(TextType.BrandName):
            content = data.get('brand_name')
            break

        if case(TextType.Time):
            content = data.get('sales_time')
            break

        if case(TextType.SalesTitle):
            content = data.get('sales_title')
            break

        if case(TextType.SalesPCT):
            content = '%s折' % data.get('sales_pct')
            break

        if case(TextType.SalesInfo):
            content = data.get('sales_info')
            break

        if case(TextType.SalesBrand):
            content = '店铺名:%s' % data.get('sales_brand')
            break

        if case():
            content = ''

    content = sensitive.Sensitive(text=content).filter_words()
    return content


def get_image_url(image_type, data):
    """
    根据图片类型获取 url

    :param image_type: 图片类型
    :param data: 图片数据
    :return: 图片的 Url
    """

    url = ''

    for case in switch.Switch(image_type):
        if case(ImageType.Goods):
            url = data.get('goods_img')
            break

        if case(ImageType.QRCode):
            url = data.get('qr_code_img')
            break

        if case(ImageType.Logo):
            url = data.get('logo_img')
            break

        if case(ImageType.Background):
            url = data.get('background_img')
            break

        if case():
            url = ''

    return url


def format_style_data(identify, size, color, texts, images):
    """
    格式化样式数据

    :return: 样式数据
    """

    # 结果
    result_data = {
        'id': identify,
        'size': size,
        'color': color,
        'texts': texts,
        'images': images
    }

    return result_data


def format_text_data(style_class, text_type, font_size, font_family, align, text_color, x, y, z_index):
    """
    格式化文字数据

    :param style_class: 样式类别
    :param text_type: 文字类型
    :param font_size: 字体大小
    :param font_family: 字体样式
    :param align: 对齐方式
    :param text_color: 文字颜色
    :param x: 位置：x
    :param y: 位置：y
    :param z_index: 层级
    :return:
    """

    data = style_class.data

    # 文本内容
    content = get_text_content(text_type, data)

    # 字体名称
    font_name = font_family or Fonts.DEFAULT_FONT_FAMILY

    # 字体方向（默认居左）
    text_align = align or 'left'

    # 字体样式
    style = {
        'align': text_align,
        'font_size': font_size,
        'font_family': font_name,
        'text_color': text_color
    }

    # 位置
    position = {
        'x': x,
        'y': y
    }

    text_data = {
        'type': text_type,
        'content': content,
        'align': text_align,
        'style': style,
        'position': position,
        'z_index': z_index
    }

    return text_data


def format_image_data(style_class, image_type, width, height, x, y, z_index):
    """
    格式化图片数据

    :param style_class: 样式类型
    :param image_type: 图片类型
    :param width: 宽度
    :param height: 高度
    :param x: 位置：x
    :param y: 位置：y
    :param z_index: 层级
    :return:
    """

    data = style_class.data

    # 图片 URL
    url = get_image_url(image_type, data)

    # 尺寸
    size = {
        'width': width,
        'height': height
    }

    # 位置
    position = {
        'x': x,
        'y': y
    }

    image_data = {
        'type': image_type,
        'size': size,
        'position': position,
        'url': url,
        'z_index': z_index
    }

    return image_data


class GoodsWxaStyle:
    """
        商品小程序分享样式
    """

    def __init__(self, post_data, style_id=0):
        """
        初始化样式

        :param post_data: 海报数据
        :param style_id: 选择的样式
        """

        self.style_id = style_id
        width, height = 750, 1334
        self.size = {"width": width, "height": height}
        self.color = (255, 255, 255)
        self.data = post_data or {}

    def get_style_one(self):
        """
            样式一
        """

        # 文字
        goods_title_data = format_text_data(self, TextType.Title, 38, None, 'left', '#333333', 50, 780, 0)
        goods_price_data = format_text_data(self, TextType.SalePrice, 38, None, 'left', '#DD3C3C', 50, 906, 1)
        hint_text_data = format_text_data(self, TextType.Hint, 28, None, 'left', '#666666', 50, 1094, 2)
        brand_name_data = format_text_data(self, TextType.BrandName, 28, None, 'left', '#999999', 160, 1184, 3)

        texts = [goods_title_data, goods_price_data, hint_text_data, brand_name_data]

        # 图片
        goods_image_data = format_image_data(self, ImageType.Goods, 750, 750, 0, 0, 0)
        qr_code_image_data = format_image_data(self, ImageType.QRCode, 250, 250, 450, 1044, 1)
        logo_image_data = format_image_data(self, ImageType.Logo, 80, 80, 50, 1164, 2)

        images = [goods_image_data, qr_code_image_data, logo_image_data]

        # 格式化数据
        return format_style_data(self.style_id, self.size, self.color, texts, images)

    def get_style_two(self):
        """
            样式二
        """

        # 文字
        goods_title_data = format_text_data(self, TextType.Title, 37, None, 'left', '#333333', 50, 520, 0)
        goods_price_data = format_text_data(self, TextType.SalePrice, 37, None, 'left', '#DD3C3C', 50, 646, 1)
        hint_text_data = format_text_data(self, TextType.Hint, 28, None, 'left', '#999999', 50, 905, 2)
        brand_name_data = format_text_data(self, TextType.BrandName, 28, None, 'left', '#666666', 160, 985, 3)

        texts = [goods_title_data, goods_price_data, hint_text_data, brand_name_data]

        # 图片
        goods_image_data = format_image_data(self, ImageType.Goods, 650, 420, 50, 50, 0)
        qr_code_image_data = format_image_data(self, ImageType.QRCode, 160, 160, 540, 890, 1)
        logo_image_data = format_image_data(self, ImageType.Logo, 80, 80, 50, 965, 2)

        images = [goods_image_data, qr_code_image_data, logo_image_data]

        # 格式化数据
        width, height = 750, 1101
        size = {"width": width, "height": height}

        return format_style_data(self.style_id, size, self.color, texts, images)

    def get_style_data(self):
        """
        获取海报样式数据

        :return: 样式数据
        """

        style_data = {}

        for case in switch.Switch(self.style_id):
            if case(0):
                style_data = self.get_style_one()
                break

            if case(1):
                style_data = self.get_style_two()
                break

            if case():
                style_data = self.get_style_one()

        return style_data


class GoodsSalesStyle:
    """
        商品促销样式
    """

    def __init__(self, post_data, style_id=0):
        """
        初始化样式

        :param post_data: 海报数据
        :param style_id: 选择的样式
        """

        self.style_id = style_id
        width, height = 750, 750
        self.size = {"width": width, "height": height}
        self.color = (255, 255, 255)
        self.data = post_data or {}

    def get_style_one(self):
        """
            样式一
        """

        # 文字
        sales_title_data = format_text_data(self, TextType.SalesTitle, 42, None, 'center', '#FFFFFF', 194, 123, 0)
        sales_pct_data = format_text_data(self, TextType.SalesPCT, 190, 'PingFang Bold', 'center', '#FFFFFF', 225, 146, 1)
        sales_info_data = format_text_data(self, TextType.SalesInfo, 90, None, 'center', '#FFFFFF', 196, 357, 2)
        sales_brand_data = format_text_data(self, TextType.SalesBrand, 30, None, 'center', '#333333', 215, 564, 3)
        time_data = format_text_data(self, TextType.Time, 30, None, 'center', '#FFFFFF', 283, 473, 4)

        texts = [sales_title_data, sales_pct_data, sales_info_data, sales_brand_data, time_data]

        # 图片
        background_image_data = format_image_data(self, ImageType.Background, 750, 750, 0, 0, 0)
        qr_code_image_data = format_image_data(self, ImageType.QRCode, 0, 0, 0, 0, 1)
        logo_image_data = format_image_data(self, ImageType.Logo, 0, 0, 0, 0, 2)

        images = [background_image_data, qr_code_image_data, logo_image_data]

        # 格式化数据
        return format_style_data(self.style_id, self.size, self.color, texts, images)

    def get_style_two(self):
        """
            样式二
        """

        # 文字
        sales_title_data = format_text_data(self, TextType.SalesTitle, 42, None, 'center', '#FFFFFF', 194, 123, 0)
        sales_pct_data = format_text_data(self, TextType.SalesPCT, 190, 'PingFang Bold', 'center', '#FFFFFF', 225, 146, 1)
        sales_info_data = format_text_data(self, TextType.SalesInfo, 90, None, 'center', '#FFFFFF', 196, 357, 2)
        sales_brand_data = format_text_data(self, TextType.SalesBrand, 30, None, 'center', '#FFFFFF', 215, 564, 3)
        time_data = format_text_data(self, TextType.Time, 30, None, 'center', '#FFFFFF', 283, 473, 4)
        hint_text = format_text_data(self, TextType.Hint, 24, 'PingFang Light', 'center', '#333333', 260, 1080, 5)

        texts = [sales_title_data, sales_pct_data, sales_info_data, sales_brand_data, time_data, hint_text]

        # 图片
        background_image_data = format_image_data(self, ImageType.Background, 750, 750, 0, 0, 0)
        qr_code_image_data = format_image_data(self, ImageType.QRCode, 250, 250, 250, 810, 1)

        images = [background_image_data, qr_code_image_data]

        # 格式化数据
        width, height = 750, 1150
        size = {"width": width, "height": height}

        return format_style_data(self.style_id, size, self.color, texts, images)

    def get_style_data(self):
        """
        获取海报样式数据

        :return: 样式数据
        """

        style_data = {}

        for case in switch.Switch(self.style_id):
            if case(0):
                style_data = self.get_style_one()
                break

            if case(1):
                style_data = self.get_style_two()
                break

            if case():
                style_data = self.get_style_one()

        return style_data
