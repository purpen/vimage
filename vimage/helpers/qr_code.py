# -*- coding: utf-8 -*-
import qrcode
import re
import io
from vimage.helpers.utils import *
from vimage.helpers.image_tools import *
from PIL import Image


# 二维码容错率
error_correct = {
    'L': qrcode.constants.ERROR_CORRECT_L,   # 7%
    'M': qrcode.constants.ERROR_CORRECT_M,   # 15%(默认)
    'Q': qrcode.constants.ERROR_CORRECT_Q,   # 25%
    'H': qrcode.constants.ERROR_CORRECT_H,   # 30%
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

        # 需要展示LOGO时进行图片合成
        result_img = self.get_logo_image(qr_img)

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
        canvas.paste(logo_image, (int(canvas_border/2), int(canvas_border/2)), logo_image)

        # 二维码和LOGO合成
        qr_code_img.paste(canvas, (size_w + int(size_w/2), size_h + int(size_h/2)), canvas)

        return qr_code_img

    def hex_to_rgb(self):
        """
            hex 色值转换成 RGB
        """

        hex_color = self.back_color

        opt = re.findall(r'(.{2})', hex_color[1:] if hex_color[0] is '#' else hex_color)

        rgb = []
        for i in range(0, len(opt)):
            rgb.append(int(opt[i], 16))

        return rgb

    def transparent_qr_code(self, qr_code_img):
        """
            透明化二维码
        """

        new_item = []

        back_color_rgb = self.hex_to_rgb()
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

    def check_url(self):
        """
            检测 URL 格式是否合法
        """

        if re.match(r'^(https|http|ftp|rtsp|mms)?:/{2}\w.+$', self.content):
            return self.content
        else:
            return None

