# -*- coding: utf-8 -*-
import io
from datetime import timedelta
from flask import Response, jsonify, current_app, request, redirect, url_for
from flask_sqlalchemy import get_debug_queries
from PIL import Image, ImageDraw, ImageFont
import requests as re
from io import BytesIO
from enum import Enum, unique
from . import main
from .. import db
from config import Config
from ..models.posterstyle import *
from ..helpers import switch

from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config


@main.route('/')
def index():
    """
        默认
    """
    return 'Index Page'


@main.route('/helloworld')
def helloworld():
    """
        测试示例
    """
    return 'Hello World!'


@main.route('/goodscard')
def showGoodsCard(post_data):
    """
        商品小程序码海报
    """

    # 海报种类：商品小程序码
    goods_card_style = GoodsCardStyle(post_data)

    # 检测商品图片比例
    goods_image_url = post_data['goods_img'] or ''
    style_type = checkImageSize(goods_image_url)

    # 选择样式数据
    style_data = {}
    draw_position = []

    for case in switch.Switch(style_type):
        if case(ImageScale.Square):
            style_data = goods_card_style.getStyleOne()
            draw_position = [(50, 990), (700, 990)]
            break

        if case(ImageScale.RectangleH):
            style_data = goods_card_style.getStyleTwo()
            draw_position = [(50, 839), (700, 839)]
            break

        if case():
            style_data = goods_card_style.getStyleOne()

    # 创建一个画布
    canvas = Canvas(style_data)

    # 保存地址
    save_path = 'vimage/resource/poster/'
    save_name = 'goods_' + str(style_data['id'])
    localfile = save_path + save_name + '.png'

    # 生成海报图片,保存到本地
    poster_image = canvas.getPoster(True, draw_position, '#999999')
    poster_image.save(localfile)

    # uploadQiniu(localfile)
    poster_image.show()


@main.route('/salescard')
def showSalesCard(post_data):
    """
        商品促销海报
    """

    # 海报种类：商品小程序码
    sales_card_style = GoodsSalesStyle(post_data)

    style_data = sales_card_style.getStyleOne()

    # 创建一个画布
    canvas = Canvas(style_data)

    # 保存地址
    save_path = 'vimage/resource/poster/'
    save_name = 'sales_' + str(style_data['id'])
    localfile = save_path + save_name + '.png'

    # 生成海报图片,保存到本地
    draw_position = [(193, 545), (553, 625)]

    poster_image = canvas.getPoster(True, draw_position, '#FFFFFF')
    poster_image.save(localfile)

    # uploadQiniu(localfile)
    poster_image.show()


@unique
class ImageScale(Enum):
    Square = 0      # 正方形
    RectangleH = 1  # 长方形，水平
    RectangleV = 2  # 长方形，垂直


def checkImageSize(image_url):
    """
        检查图片尺寸比例，选择海报样式
    """

    response = re.get(image_url)
    image = Image.open(BytesIO(response.content)).convert('RGBA')

    scale = image.size[0] / image.size[1]

    if scale == 1.0:
        return ImageScale.Square

    elif scale > 1.0:
        return ImageScale.RectangleH

    elif scale < 1.0:
        return ImageScale.RectangleV

    else:
        return ImageScale.Square


def drawRectangle(image, position, color):
    """
        绘制矩形
    """

    #  直线的位置、长短
    line_position = position or [(0, 1), (100, 1)]

    draw_image = ImageDraw.Draw(image)
    draw_image.rectangle(line_position, fill=color)

    return image


def pasteImage(back_image, paste_image):
    """
    合成图片

    :param back_image: 背景图片
    :param paste_image: 合成上去的图片
    :return: 结果图片
    """

    # 图像的尺寸大小
    result_size = paste_image.size or {}
    width = result_size['width']
    height = result_size['height']

    # 图像合成的位置
    result_position = paste_image.position or {}
    left = result_position['left']
    top = result_position['top']

    # 要合成到背景的图像
    result_image = paste_image.image

    if result_image is not None:
        result_image = result_image.resize((width, height), 0, (width/4, 0, width, height))
        # 对图片合成
        back_image.paste(result_image, (left, top), result_image)

    return back_image


def drawText(back_image, creat_text):
    """
    绘制文字

    :param back_image: 背景图片
    :param creat_text: 需要绘制的文字
    :return: 绘制完成的图片
    """

    position = creat_text.position or {}
    left = position['left'] or 0
    top = position['top'] or 0

    # 绘制文字
    draw_font = ImageFont.truetype(creat_text.font_family, creat_text.font_size)

    draw_image = ImageDraw.Draw(back_image)
    draw_image.text([left, top], creat_text.content, font=draw_font, align=creat_text.align, fill=creat_text.text_color)

    return back_image


class TextObject:
    """
        文字对象
    """

    def __init__(self, data):
        """
        文字类型

        :param data: 文字数据
        """

        text_data = data or {}
        text_style = text_data['style'] or {}

        self.type = data['type']  # 类型（标题/内容/附加信息等）
        self.content = data['content']  # 默认内容
        self.position = data['position']  # 区域位置
        self.align = data['align']
        self.font_size = text_style['font_size']  # 字体大小
        self.font_family = text_style['font_family']  # 字体样式
        self.text_color = text_style['text_color']  # 文字颜色
        self.zindex = data['zindex']  # 层级（文字叠加）


class ImageObject:
    """
        图片对象
    """

    def __init__(self, data):
        """
        图片类型

        :param data: 图片数据
        """

        image_data = data or {}

        self.type = image_data['type']  # 类型（主图/背景/二维码/LOGO/边框等）
        self.size = image_data['size']  # 尺寸
        self.position = image_data['position']  # 位置
        self.url = image_data['url']  # url 路径
        self.zindex = image_data['zindex']  # 层级（叠加顺序）

        if len(self.url) > 0:
            response = re.get(self.url)
            self.image = Image.open(BytesIO(response.content)).convert('RGBA')  # 图片

        else:
            self.image = None


class Canvas:
    def __init__(self, data):
        """
            海报画布
        """

        canvas_data = data or {}

        self.style_id = canvas_data['id'] or 0  # id
        self.color = canvas_data['color'] or (255, 255, 255)  # 背景颜色
        self.texts = canvas_data['texts'] or []  # 文字
        self.images = canvas_data['images'] or []  # 图片
        canvas_size = canvas_data['size'] or {}  # 尺寸
        self.width = canvas_size['width'] or 0  # 宽度
        self.height = canvas_size['height'] or 0  # 高度

    def getCanvas(self):
        """
        创建画布

        :return: 输出画布背景
        """

        canvas_image = Image.new('RGBA', (self.width, self.height), self.color)

        return canvas_image

    def getPoster(self, isDrawRectangle, draw_position, draw_color):
        """
        创建海报图片

        :return: 海报图片
        """

        # 生成画布
        canvas = self.getCanvas()

        # 根据图像位置层级，对数据进行排序
        sort_images = sorted(self.images, key=lambda e: e.get('zindex'))
        # 获取图像数据
        for imageItem in sort_images:
            creat_image = ImageObject(imageItem)

            # 把图像合成到画布
            canvas = pasteImage(canvas, creat_image)

        # 是否绘制
        if isDrawRectangle is True:
            drawRectangle(canvas, draw_position, draw_color)

        # 根据文字位置层级，对数据进行排序
        sort_texts = sorted(self.texts, key=lambda e: e.get('zindex'))
        # 获取文字数据
        for textItem in sort_texts:
            creat_text = TextObject(textItem)

            # 在画布上绘制文字
            canvas = drawText(canvas, creat_text)

        return canvas


def uploadQiniu(localfile):
    """
        上传图片到七牛
    """

    q = Auth(Config.QINIU_ACCESS_KEY, Config.QINIU_ACCESS_SECRET)
    bucket_name = Config.QINIU_BUCKET_NAME
    key = 'my-poster-image.png'
    token = q.upload_token(bucket_name, key, 3600)

    ret, info = put_file(token, key, localfile)

    print(info)

    assert ret['key'] == key
    assert ret['hash'] == etag(localfile)
