# -*- coding: utf-8 -*-
from vimage.helpers.poster_style_element import *
from vimage.helpers.switch import Switch
from vimage.helpers.sensitive import PickSensitive
from vimage.constant import *


def get_text_content(text_type, data):
    """
    根据类型获取对应的文字内容

    :param text_type: 文字类型
    :param data: 文字数据
    :return: 文字内容
    """

    text_content_data = {
        TextType.Title: data.get('title'),
        TextType.SalePrice: data.get('sale_price'),
        TextType.Hint: data.get('hint_text'),
        TextType.BrandName: data.get('brand_name'),
        TextType.Time: data.get('time'),
        TextType.SalesTitle: data.get('sales_title'),
        TextType.SalesPCT: data.get('sales_pct'),
        TextType.SalesInfo: data.get('sales_info'),
        TextType.SalesBrand: data.get('sales_brand'),
        TextType.OtherInfo1: data.get('other_1'),
        TextType.OtherInfo2: data.get('other_2'),
        TextType.SymbolPCT: data.get('symbol_pct'),
        TextType.SymbolOff: data.get('symbol_off'),
        TextType.BrandSlogan: data.get('brand_slogan'),
        TextType.Describe: data.get('describe'),
        TextType.Nickname: data.get('nickname'),
        TextType.City: data.get('city'),
    }

    content = text_content_data.get(text_type)

    # content = PickSensitive(text=content).replace_filter_words()

    return content


def get_image_url(image_type, data):
    """
    根据图片类型获取 url

    :param image_type: 图片类型
    :param data: 图片数据
    :return: 图片的 Url
    """

    image_url_data = {
        ImageType.Goods: data.get('goods_img'),
        ImageType.QRCode: data.get('qr_code_img'),
        ImageType.Logo: data.get('logo_img'),
        ImageType.Background: data.get('background_img'),
        ImageType.Modify: data.get('modify_img'),
        ImageType.WxaCode: data.get('wxa_code_img'),
        ImageType.Avatar: data.get('avatar_img'),
        ImageType.BrandLogo: data.get('brand_logo_img'),
        ImageType.Guess: data.get('guess_img'),
    }

    url = image_url_data.get(image_type)

    return url


def format_text_data(post_data, text, text_type, font_size, font_family, align, text_color, x, y, spacing, z_index, width=None):
    """
    格式化文字数据

    :param post_data: 样式展示内容数据
    :param text: 文字内容
    :param text_type: 文字类型
    :param font_size: 字体大小
    :param font_family: 字体样式
    :param align: 对齐方式
    :param text_color: 文字颜色
    :param x: 位置：x
    :param y: 位置：y
    :param spacing: 行间距
    :param z_index: 层级
    :param width: 宽度
    :return:
    """

    data = post_data or {}

    # 文本内容
    content = get_text_content(text_type, data) if not text else text
    print ('======== %s' % content)
    content.replace('\n', '')

    # 字体名称
    font_name = font_family or Fonts.DEFAULT_FONT_FAMILY

    # 字体方向（默认居左）
    text_align = align or Fonts.DEFAULT_FONT_ALIGN

    # 字体样式
    style = {
        'align': text_align,
        'font_size': font_size,
        'font_family': font_name,
        'text_color': text_color,
        'line_spacing': spacing
    }

    # 位置
    position = (int(x), int(y))

    text_data = {
        'type': text_type,
        'content': content,
        'align': text_align,
        'style': style,
        'position': position,
        'z_index': z_index,
        'width': width
    }

    return text_data


def format_image_data(post_data, url, path, image_type, width, height, radius, x, y, z_index):
    """
    格式化图片数据

    :param post_data: 样式展示数据
    :param url: 图片地址
    :param path: 本地路径
    :param image_type: 图片类型
    :param width: 宽度
    :param height: 高度
    :param radius: 圆角半径
    :param x: 位置：x
    :param y: 位置：y
    :param z_index: 层级
    :return:
    """

    data = post_data or {}

    # 图片 URL
    img_url = get_image_url(image_type, data) if not url else url

    # 路径
    img_path = None if not path else path

    # 尺寸
    size = (int(width), int(height))

    # 位置
    position = (int(x), int(y))

    image_data = {
        'type': image_type,
        'size': size,
        'position': position,
        'radius': radius,
        'url': img_url,
        'path': img_path,
        'z_index': z_index
    }

    return image_data


def format_shape_data(shape_type, position, width, color, out_color, z_index):
    """
    格式化图形元素数据

    :param shape_type: 形状类型
    :param position: 位置 [(x1, y1), (x2, y2)]
    :param width: 宽度
    :param color: 填充颜色
    :param out_color: 边框颜色
    :param z_index: 层级
    :return:
    """

    shape_data = {
        'type': shape_type,
        'width': width or 1,
        'position': position,
        'color': color,
        'out_color': out_color,
        'z_index': z_index
    }

    return shape_data


def format_style_data(identify, size, color, texts, images, shapes):
    """
    格式化样式数据

    :param identify: 样式id
    :param size: 尺寸大小
    :param color: 颜色
    :param texts: 文字内容
    :param images: 图片内容
    :param shapes: 图形内容
    :return:
    """

    # 结果
    style_data = {
        'id': identify,
        'size': size,
        'color': color,
        'texts': texts,
        'images': images,
        'shapes': shapes
    }

    return style_data
