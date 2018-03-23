# -*- coding: utf-8 -*-
from enum import Enum, unique
from ..helpers import switch, sensitive


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


def getContent(text_type, data):
    """
        根据类型获取对应的文字内容
    """

    content = ''

    for case in switch.Switch(text_type):
        if case(TextType.Title):
            content = data['title'] or ''
            break

        if case(TextType.SalePrice):
            content = ('￥' + data['sale_price']) or ''
            break

        if case(TextType.Hint):
            content = data['hint_text'] or '长按识别小程序码访问'
            break

        if case(TextType.BrandName):
            content = data['brand_name'] or ''
            break

        if case(TextType.Time):
            content = data['time_text'] or ''
            break

        if case(TextType.SalesTitle):
            content = data['sales_title'] or ''
            break

        if case(TextType.SalesPCT):
            content = (data['sales_pct'] + '折') or ''
            break

        if case(TextType.SalesInfo):
            content = data['sales_info'] or ''
            break

        if case(TextType.SalesBrand):
            content = ('店铺名：' + data['sales_brand']) or ''
            break

        if case():
            content = ''

    content = sensitive.Sensitive(text=content).filterWords()
    return content


def getImageUrl(image_type, data):
    """
        根据图片类型获取 url
    """

    url = ''

    for case in switch.Switch(image_type):
        if case(ImageType.Goods):
            url = data['goods_img'] or ''
            break

        if case(ImageType.QRCode):
            url = data['qrcode_img'] or ''
            break

        if case(ImageType.Logo):
            url = data['logo_img'] or ''
            break

        if case(ImageType.Background):
            url = data['background_img'] or ''
            break

        if case():
            url = ''

    return url


def getStyleData(identify, size, color, texts, images):
    """
    格式化样式数据

    :return: 样式数据
    """

    # 结果
    result_data = {
        "id": identify,
        "size": size,
        "color": color,
        "texts": texts,
        "images": images
    }

    return result_data


def getTextData(style_class, text_type, font_size, font_family, align, text_color, x, y, zindex):
    """
    格式化文字数据

    :return: 样式数据
    """

    data = style_class.data

    # 文本内容
    content = getContent(text_type, data)

    # 字体名称
    font_name = font_family or 'PingFang'

    # 字体方向（默认巨左）
    text_align = align or 'left'

    # 字体样式
    style = {
        "font_size": font_size,
        "font_family": font_name,
        "text_color": text_color
    }

    # 位置
    position = {
        "left": x,
        "top": y
    }

    text_data = {
        "type": text_type,
        "content": content,
        "align": text_align,
        "style": style,
        "position": position,
        "zindex": zindex
    }

    return text_data


def getImageData(style_class, image_type, width, height, x, y, zindex):
    """
    格式化图片数据

    :return: 样式数据
    """

    data = style_class.data

    # 图片 URL
    url = getImageUrl(image_type, data)

    # 尺寸
    size = {
        "width": width,
        "height": height
    }

    # 位置
    position = {
        "left": x,
        "top": y
    }

    image_data = {
        "type": image_type,
        "size": size,
        "position": position,
        "url": url,
        "zindex": zindex
    }

    return image_data


class GoodsCardStyle:
    """
        商品分享图片样式
    """

    def __init__(self, post_data):
        """
            初始化样式
        """

        self.identify = 0
        width, height = 750, 1334
        self.size = {"width": width, "height": height}
        self.color = (255, 255, 255)
        self.data = post_data or {}

    def getStyleOne(self):
        """
            样式一
        """

        # 文字
        goods_title_data = getTextData(self, TextType.Title, 38, None, None, '#333333', 50, 780, 0)
        goods_price_data = getTextData(self, TextType.SalePrice, 38, None, None, '#DD3C3C', 50, 906, 1)
        hint_text_data = getTextData(self, TextType.Hint, 28, None, None, '#666666', 50, 1094, 2)
        brand_name_data = getTextData(self, TextType.BrandName, 28, None, None, '#999999', 160, 1184, 3)

        texts = [goods_title_data, goods_price_data, hint_text_data, brand_name_data]

        # 图片
        goods_image_data = getImageData(self, ImageType.Goods, 750, 750, 0, 0, 0)
        qrcode_image_data = getImageData(self, ImageType.QRCode, 250, 250, 450, 1044, 1)
        logo_image_data = getImageData(self, ImageType.Logo, 80, 80, 50, 1164, 2)

        images = [goods_image_data, qrcode_image_data, logo_image_data]

        # 格式化数据
        return getStyleData(self.identify, self.size, self.color, texts, images)

    def getStyleTwo(self):
        """
            样式二
        """

        # 文字
        goods_title_data = getTextData(self, TextType.Title, 37, None, None, '#333333', 50, 520, 0)
        goods_price_data = getTextData(self, TextType.SalePrice, 37, None, None, '#DD3C3C', 50, 646, 1)
        hint_text_data = getTextData(self, TextType.Hint, 28, None, None, '#999999', 50, 905, 2)
        brand_name_data = getTextData(self, TextType.BrandName, 28, None, None, '#666666', 160, 985, 3)

        texts = [goods_title_data, goods_price_data, hint_text_data, brand_name_data]

        # 图片
        goods_image_data = getImageData(self, ImageType.Goods, 650, 420, 50, 50, 0)
        qrcode_image_data = getImageData(self, ImageType.QRCode, 160, 160, 540, 890, 1)
        logo_image_data = getImageData(self, ImageType.Logo, 80, 80, 50, 965, 2)

        images = [goods_image_data, qrcode_image_data, logo_image_data]

        # 格式化数据
        width, height = 750, 1101
        size = {"width": width, "height": height}

        return getStyleData(self.identify, size, self.color, texts, images)


class GoodsSalesStyle:
    """
        商品促销样式
    """

    def __init__(self, post_data):
        """
            初始化样式
        """

        self.identify = 100
        width, height = 750, 750
        self.size = {"width": width, "height": height}
        self.color = (255, 255, 255)
        self.data = post_data or {}

    def getStyleOne(self):
        """
            样式一
        """

        # 文字
        salse_title_data = getTextData(self, TextType.SalesTitle, 42, None, 'center', '#FFFFFF', 194, 123, 0)
        sales_pct_data = getTextData(self, TextType.SalesPCT, 190, None, 'center', '#FFFFFF', 225, 146, 1)
        sales_info_data = getTextData(self, TextType.SalesInfo, 90, None, 'center', '#FFFFFF', 196, 357, 2)
        sales_brand_data = getTextData(self, TextType.SalesBrand, 30, None, 'center', '#333333', 215, 564, 3)
        time_data = getTextData(self, TextType.Time, 30, None, 'center', '#FFFFFF', 283, 473, 4)

        texts = [salse_title_data, sales_pct_data, sales_info_data, sales_brand_data, time_data]

        # 图片
        background_image_data = getImageData(self, ImageType.Background, 750, 750, 0, 0, 0)
        qrcode_image_data = getImageData(self, ImageType.QRCode, 0, 0, 0, 0, 1)
        logo_image_data = getImageData(self, ImageType.Logo, 0, 0, 0, 0, 2)

        images = [background_image_data, qrcode_image_data, logo_image_data]

        # 格式化数据
        return getStyleData(self.identify, self.size, self.color, texts, images)

