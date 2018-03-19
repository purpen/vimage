# -*- coding: utf-8 -*-
import io
from datetime import timedelta
from flask import Response, jsonify, current_app, request, redirect, url_for
from flask_sqlalchemy import get_debug_queries
from PIL import Image, ImageDraw, ImageFont

from enum import Enum, unique
from . import main
from .. import db


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


class Canvas():
    def __init__(self, data):
        """
        画布

        :param data: 数据
        """

        canvas_data = data or {}

        self.style_id = canvas_data['style_id'] or 0
        canvas_size = canvas_data['size'] or {}
        self.width = canvas_size['width'] or 10
        self.height = canvas_size['height'] or 10
        self.color = canvas_data['color'] or (255, 255, 255)
        self.texts = canvas_data['texts'] or []
        self.images = canvas_data['images'] or []

    def creatCanvas(self):
        """
        创建画布

        :return: 输出画布背景
        """

        canvas_image = Image.new('RGB', (self.width, self.height), self.color)

        return canvas_image

    def pasteImage(self, back_image, paste_image):
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

        # 图像范围
        result_region = paste_image.image
        result_region = result_region.resize((width, height))

        # 对图片合成
        back_image.paste(result_region, (left, top), mask=result_region)

        return back_image

    def drawText(self, back_image, creat_text):
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
        draw_image.text([left, top], creat_text.content, font=draw_font, fill=creat_text.text_color)

        return back_image

    def creatPoster(self):
        """
        创建海报图片

        :return: 海报图片
        """

        # 生成画布
        canvas = self.creatCanvas()

        # 根据图像位置层级，对数据进行排序
        sort_images = sorted(self.images, key=lambda e: e.get('zindex'))

        # 获取图像数据
        for imageItem in sort_images:
            creat_image = CreatImage(imageItem)

            # 把图像合成到画布
            canvas = self.pasteImage(canvas, creat_image)

        # 根据文字位置层级，对数据进行排序
        sort_texts = sorted(self.texts, key=lambda e: e.get('zindex'))

        # 获取文字数据
        for textItem in sort_texts:
            creat_text = CreatText(textItem)

            # 在画布上绘制文字
            canvas = self.drawText(canvas, creat_text)

        return canvas


@unique
class ImageType(Enum):
    Main = 0  # 主图
    Background = 1  # 背景
    QRCode = 2  # 二维码
    Logo = 3  # logo
    Border = 4  # 边框
    Modify = 5  # 修饰
    Mask = 6  # 蒙版


class CreatImage:
    def __init__(self, data):
        """
        图片类型

        :param data: 图片数据
        """

        image_data = data or {}

        self.type = image_data['type']  # 图片类型（主图/背景/二维码/LOGO/边框等）
        self.size = image_data['size']  # 图片尺寸
        self.position = image_data['position']  # 图片位置
        self.path = image_data['path']  # 图片路径
        self.zindex = image_data['zindex']  # 图片层级（叠加顺序）
        self.image = Image.open(self.path, 'r')  # 图片


@unique
class TextType(Enum):
    Title = 0  # 标题
    Content = 1  # 内容
    Info = 2  # 其他信息


class CreatText():
    def __init__(self, data):
        """
        文字类型

        :param data: 文字数据
        """

        text_data = data or {}
        text_style = text_data['style'] or {}

        self.type = data['type']  # 文字类型（标题/内容/附加信息等）
        self.content = data['content']  # 默认文字内容
        self.position = data['position']  # 文字区域位置
        self.font_size = text_style['font_size']  # 字体大小
        self.font_family = text_style['font_family']  # 字体样式
        self.text_color = text_style['text_color']  # 文字颜色
        self.zindex = data['zindex']  # 文字层级（文字叠加时）


def testPosterData(data_post):
    """
    海报测试数据

    :return: 海报数据
    """

    data = data_post or {}

    # 文字内容数据
    texts = [{'type': TextType.Title,
              'content': data['title'],
              'style': {'font_size': 50, 'font_family': 'PingFang', 'text_color': '#FFFFFF'},
              'position': {'left': 112, 'top': 135},
              'zindex': 0
              },
             {'type': TextType.Content,
              'content': data['subtitle'],
              'style': {'font_size': 36, 'font_family': 'PingFang', 'text_color': '#FFFFFF'},
              'position': {'left': 112, 'top': 210},
              'zindex': 1
              },
             {'type': TextType.Content,
              'content': data['content'],
              'style': {'font_size': 144, 'font_family': 'Arial Narrow Bold', 'text_color': '#FFFFFF'},
              'position': {'left': 112, 'top': 255},
              'zindex': 2
              },
             {'type': TextType.Content,
              'content': data['add_content'],
              'style': {'font_size': 40, 'font_family': 'PingFang', 'text_color': '#FFFFFF'},
              'position': {'left': 264, 'top': 1042},
              'zindex': 3
              }]

    # 图片内容数据
    images = [{'type': ImageType.Main,
               'size': {'width': 750, 'height': 1334},
               'position': {'left': 0, 'top': 0},
               'path': 'vimage/resource/mainImage/poster_main_0.png',
               'zindex': 0
               },
              {'type': ImageType.Border,
               'size': {'width': 670, 'height': 1130},
               'position': {'left': 40, 'top': 160},
               'path': 'vimage/resource/border/poster_border_0.png',
               'zindex': 2
               },
              {'type': ImageType.Logo,
               'size': {'width': 142, 'height': 72},
               'position': {'left': 570, 'top': 40},
               'path': 'vimage/resource/logo/poster_logo_0.png',
               'zindex': 1
               },
              {'type': ImageType.QRCode,
               'size': {'width': 170, 'height': 170},
               'position': {'left': 290, 'top': 1145},
               'path': 'vimage/resource/qrcode/poster_qrcode_0.png',
               'zindex': 3
               }]

    # 样式ID
    style_id = 0

    # 尺寸大小
    size = {'width': 750, 'height': 1334}

    # 颜色
    color = (0, 0, 0)

    poster_data = {'style_id': style_id,
                   'size': size,
                   'color': color,
                   'texts': texts,
                   'images': images
                   }

    return poster_data


def testInvitationData():
    """
    邀请函测试数据

    :return: 海报数据
    """

    # 文字内容数据
    texts = [{'type': TextType.Title,
              'content': '浙江省工业设计协会',
              'style': {'font_size': 30, 'font_family': 'PingFang', 'text_color': '#000000'},
              'position': {'left': 239.5, 'top': 242},
              'zindex': 0
              },
             {'type': TextType.Content,
              'content': '浙江传统产业设计再制造计划启动仪式',
              'style': {'font_size': 34, 'font_family': 'PingFang', 'text_color': '#000000'},
              'position': {'left': 86, 'top': 393},
              'zindex': 1
              },
             {'type': TextType.Content,
              'content': '暨传统产业设计再制造高峰论坛',
              'style': {'font_size': 32, 'font_family': 'PingFang', 'text_color': '#000000'},
              'position': {'left': 151, 'top': 450},
              'zindex': 2
              },
             {'type': TextType.Content,
              'content': '雷海波',
              'style': {'font_size': 60, 'font_family': 'PingFang', 'text_color': '#000000'},
              'position': {'left': 285, 'top': 627},
              'zindex': 3
              },
             {'type': TextType.Content,
              'content': '莅临并作嘉宾演讲！',
              'style': {'font_size': 32, 'font_family': 'PingFang', 'text_color': '#000000'},
              'position': {'left': 231, 'top': 804},
              'zindex': 4
              },
             {'type': TextType.Content,
              'content': '扫 码 了 解 更 多',
              'style': {'font_size': 20, 'font_family': 'PingFang', 'text_color': '#000000'},
              'position': {'left': 298, 'top': 1120},
              'zindex': 5
              }]

    # 图片内容数据
    images = [{'type': ImageType.Background,
               'size': {'width': 750, 'height': 1334},
               'position': {'left': 0, 'top': 0},
               'path': 'vimage/resource/background/invitation_back_0.png',
               'zindex': 0
               },
              {'type': ImageType.QRCode,
               'size': {'width': 180, 'height': 180},
               'position': {'left': 285, 'top': 917},
               'path': 'vimage/resource/qrcode/poster_qrcode_0.png',
               'zindex': 1
               }]

    # 样式ID
    style_id = 100

    # 尺寸大小
    size = {'width': 750, 'height': 1334}

    # 颜色
    color = (0, 0, 0)

    invitation_data = {'style_id': style_id,
                   'size': size,
                   'color': color,
                   'texts': texts,
                   'images': images
                   }

    return invitation_data


@main.route('/poster')
def showPoster(data_post):
    """
        展示生成的海报
    """

    test_data = testPosterData(data_post)

    # 创建一个画布
    canvas = Canvas(test_data)

    save_path = 'vimage/resource/poster/'
    save_name = 'poster_' + str(test_data['style_id'])

    # 生成海报图片
    poster_image = canvas.creatPoster()
    poster_image.save(save_path + save_name + '.jpg')
    poster_image.show()

    # Flask 前端显示类型
    # response = Response(poster_image, mimetype='image/jpeg')

    return '海报生成 = success!'
