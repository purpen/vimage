# -*- coding:utf-8 -*-
from vimage.helpers.poster_style_format import *
from vimage.constant import *


class GoodsGifStyle:
    """
        动态海报样式
    """

    def __init__(self, post_data, style_id=0):
        """
        初始化样式

        :param post_data: 海报数据
        :param style_id: 选择的样式
        """

        self.style_id = style_id
        width, height = Size.POSTER_IMAGE_SIZE['width'], Size.POSTER_IMAGE_SIZE['height']
        self.size = (width, height)
        self.color = (255, 255, 255)
        self.data = post_data or {}

        # 样式id参数绑定的数据方法
        self.styles = {'1': self.get_style_one()}

    def get_style_one(self):
        """
            样式一
        """

        # 文字
        sales_info_data = format_text_data(self.data, None, TextType.SalesInfo, 26, 'PingFang Bold', 'left', '#333333', 123, 1092, None, 0)

        texts = [sales_info_data]

        # 图片
        qr_code_image_data = format_image_data(self.data, None, ImageType.QRCode, 190, 190, 0, 520, 1052, 0)

        images = [qr_code_image_data]

        # 图形元素
        draw_rectangle_data = format_shape_data(DrawShapeType.Rectangle, [(0, 1052), (470, 1242)], 1, '#CFD6EC', None, 0)
        draw_line1_data = format_shape_data(DrawShapeType.Line, [(94, 1074), (159, 1029)], 3, '#333333', None, 1)
        draw_line2_data = format_shape_data(DrawShapeType.Line, [(394, 1264), (459, 1219)], 3, '#333333', None, 2)

        shapes = [draw_rectangle_data, draw_line1_data, draw_line2_data]

        # 格式化数据
        color = (255, 255, 255, 0)
        return format_style_data(self.style_id, self.size, color, texts, images, shapes)

    def get_style_data(self):
        """
        获取海报样式数据

        :return: 样式数据
        """

        style_id = str(self.style_id)

        style_data = self.styles.get(style_id)

        return style_data
