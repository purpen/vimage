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


def getContent(text_type, data):
    """
        根据类型获取对应的文字内容
    """

    content = ''

    for case in switch.Switch(text_type):
        if case(TextType.Title):
            content = data['title'] or ''
            content = sensitive.Sensitive(text=content).filterWords()
            break

        if case(TextType.SalePrice):
            content = data['sale_price'] or ''
            break

        if case(TextType.Hint):
            content = data['hint_text'] or '长按识别小程序码访问'
            break

        if case(TextType.BrandName):
            content = data['brand_name'] or ''
            break

        if case():
            content = ''

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

    def getTextData(self, text_type, font_size, font_family, align, text_color, x, y, zindex):
        """
        格式化文字数据

        :return: 样式数据
        """

        data = self.data

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

    def getImageData(self, image_type, width, height, x, y, zindex):
        """
        格式化图片数据

        :return: 样式数据
        """

        data = self.data

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

    def getStyleOne(self):
        """
            样式一
        """

        # 文字
        goods_title_data = self.getTextData(TextType.Title, 38, None, None, '#333333', 50, 780, 0)
        goods_price_data = self.getTextData(TextType.SalePrice, 38, None, None, '#DD3C3C', 50, 906, 1)
        hint_text_data = self.getTextData(TextType.Hint, 28, None, None, '#666666', 50, 1094, 2)
        brand_name_data = self.getTextData(TextType.BrandName, 28, None, None, '#999999', 160, 1184, 3)

        texts = [goods_title_data, goods_price_data, hint_text_data, brand_name_data]

        # 图片
        goods_image_data = self.getImageData(ImageType.Goods, 750, 750, 0, 0, 0)
        qrcode_image_data = self.getImageData(ImageType.QRCode, 250, 250, 450, 1044, 1)
        logo_image_data = self.getImageData(ImageType.Logo, 80, 80, 50, 1164, 2)

        images = [goods_image_data, qrcode_image_data, logo_image_data]

        # 格式化数据
        return getStyleData(self.identify, self.size, self.color, texts, images)

    def getStyleTwo(self):
        """
            样式二
        """

        # 文字
        goods_title_data = self.getTextData(TextType.Title, 37, None, None, '#333333', 50, 520, 0)
        goods_price_data = self.getTextData(TextType.SalePrice, 37, None, None, '#DD3C3C', 50, 646, 1)
        hint_text_data = self.getTextData(TextType.Hint, 28, None, None, '#999999', 50, 905, 2)
        brand_name_data = self.getTextData(TextType.BrandName, 28, None, None, '#666666', 160, 985, 3)

        texts = [goods_title_data, goods_price_data, hint_text_data, brand_name_data]

        # 图片
        goods_image_data = self.getImageData(ImageType.Goods, 650, 420, 50, 50, 0)
        qrcode_image_data = self.getImageData(ImageType.QRCode, 160, 160, 540, 890, 1)
        logo_image_data = self.getImageData(ImageType.Logo, 80, 80, 50, 965, 2)

        images = [goods_image_data, qrcode_image_data, logo_image_data]

        # 格式化数据
        width, height = 750, 1101
        size = {"width": width, "height": height}

        return getStyleData(self.identify, size, self.color, texts, images)
