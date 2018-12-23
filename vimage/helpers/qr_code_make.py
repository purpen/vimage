# -*- coding: utf-8 -*-
from flask import current_app
import qrcode
import re
import io
from vimage.helpers.utils import *
from vimage.helpers.image_tools import *
from PIL import Image, ImageColor, ImageDraw, ImageFont

# 二维码容错率
error_correct = {
    'L': qrcode.constants.ERROR_CORRECT_L,  # 7%
    'M': qrcode.constants.ERROR_CORRECT_M,  # 15%(默认)
    'Q': qrcode.constants.ERROR_CORRECT_Q,  # 25%
    'H': qrcode.constants.ERROR_CORRECT_H,  # 30%
}


class QRCodeObject:
    """
        二维码对象
    """

    def __init__(self, post_data):
        """
        初始化一个二维码对象

        :param post_data: 数据内容
        """

        data = post_data or {}
        self.type = data.get('type', 1)
        self.content = data.get('content')
        self.logo_img = data.get('logo_img')
        self.version = data.get('version', 4)
        self.box_size = data.get('box_size', 10)
        self.border = data.get('border', 1)
        self.error_correct = data.get('error_correct', 'M')
        self.fill_color = data.get('fill_color', '#000000')
        self.back_color = data.get('back_color', '#FFFFFF')
        self.gradient = data.get('gradient')
        self.g_direction = data.get('g_direction', 0)
        self.hint_text = data.get('hint_text')
        self.background = data.get('background')

    def create_qr_code(self):
        """
            生成二维码
        """

        # 网址类型时检测 url 是否合法
        content = self.check_url() if self.type == 2 else self.content

        if not content:
            return None

        qr_code = qrcode.QRCode(version=self.version,
                                error_correction=error_correct.get(self.error_correct),
                                box_size=self.box_size,
                                border=self.border)
        qr_code.add_data(content)
        qr_code.make(fit=True)

        # 生成二维码图片
        qr_img = qr_code.make_image(fill_color=self.fill_color, back_color=self.back_color).convert('RGBA')

        # 是否需要渐变色二维码
        qr_img = qr_img if not self.gradient else self.gradient_qr_code(qr_img)

        # 需要展示LOGO时进行图片合成
        result_qr_code = self.get_logo_image(qr_img)

        # 是否添加文字
        result_img = result_qr_code if not self.hint_text else self.add_hint_text(result_qr_code)

        return result_img

    def get_logo_image(self, qr_code_img):
        """
            获取 LOGO 图片
        """

        if not self.logo_img:
            return qr_code_img

        scale = 4
        qr_img_w, qr_img_h = qr_code_img.size
        size_w = int(qr_img_w / scale)
        size_h = int(qr_img_h / scale)

        # LOGO 放置的画布
        canvas_border = 6
        canvas = Image.new('RGBA', (size_w + canvas_border, size_h + canvas_border), 'white')

        # 加载 LOGO 图片，调整大小，合成
        logo_image = load_url_image(self.logo_img)
        logo_image = logo_image.resize((size_w, size_h), Image.ANTIALIAS)
        canvas.paste(logo_image, (int(canvas_border / 2), int(canvas_border / 2)), logo_image)

        # 二维码和LOGO合成
        qr_code_img.paste(canvas, (size_w + int(size_w / 2), size_h + int(size_h / 2)))

        return qr_code_img

    def transparent_qr_code(self, qr_code_img):
        """
            透明化二维码
        """

        new_item = []

        back_color_rgb = hex_to_rgb(self.fill_color)
        r = back_color_rgb[0]
        g = back_color_rgb[1]
        b = back_color_rgb[2]

        for item in qr_code_img.getdata():
            if item[0] == r and item[1] == g and item[2] == b:
                new_item.append((255, 255, 255, 0))

            else:
                new_item.append(item)

        qr_code_img.putdata(new_item)

        return qr_code_img

    def gradient_qr_code(self, qr_code_img):
        """
            渐变色背景二维码
        """

        original_qr_code_img = self.transparent_qr_code(qr_code_img)

        # 色值转换为 RGB
        color_rgb_1 = ImageColor.getrgb(self.gradient[0])
        color_rgb_2 = ImageColor.getrgb(self.gradient[1])

        # 生成渐变色背景
        back_img = gradient_color(color1=color_rgb_1, color2=color_rgb_2,
                                  w=qr_code_img.size[0], h=qr_code_img.size[1], direction=self.g_direction)

        # 二维码&背景合成
        back_img.paste(original_qr_code_img, (0, 0), original_qr_code_img)

        return back_img

    def add_hint_text(self, qr_code_img):
        """
            添加提示文字
        """

        # 画布
        width = qr_code_img.size[0] + 20
        height = qr_code_img.size[1] + 100

        canvas_color = (255, 255, 255, 0) if not self.background else (255, 255, 255, 255)
        canvas = Image.new('RGBA', (width, height), canvas_color)

        # 字体的样式
        font_family = 'PingFang Regular'
        font_path = '%s%s%s' % (current_app.config['MAKE_IMAGE_FONTS_PATH'], font_family, '.ttf')
        draw_font = ImageFont.truetype(font=font_path, size=28)

        # 重新计算文字内容，保持居中，设置文字的位置
        text_size = draw_font.getsize(self.hint_text)
        position_x = (canvas.size[0] - text_size[0]) / 2
        position_y = qr_code_img.size[1] + 30
        position = (position_x, position_y)

        # 二维码放置到画布
        canvas.paste(qr_code_img, (10, 10))

        # 文字的样式配置
        ImageDraw.Draw(canvas).text(xy=position, text=self.hint_text, fill='#333333', font=draw_font, align='center')

        return canvas

    def check_url(self):
        """
            检测 URL 格式是否合法
        """

        if re.match(r'^(https|http|ftp|rtsp|mms)?:/{2}\w.+$', self.content):
            return self.content
        else:
            return None
