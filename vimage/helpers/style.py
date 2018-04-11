# -*- coding: utf-8 -*-
from vimage.helpers.style_format import *
from vimage.constant import *
from vimage.models.asset import *


def take_view_url(asset_id):
    """
    从数据库获取图片素材链接

    :param asset_id: 查询主键
    :return: 图片链接
    """

    image_url = ''

    asset = Asset.query.filter_by(id=asset_id).first()
    if asset:
        image_url = asset.view_url

    return image_url


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
        width, height = Size.POSTER_IMAGE_SIZE['width'], Size.POSTER_IMAGE_SIZE['height']
        self.size = {"width": width, "height": height}
        self.color = (255, 255, 255)
        self.data = post_data or {}

        # 样式id参数绑定的数据方法
        self.styles = {'1': self.get_style_one(),
                       '2': self.get_style_two()}

    def get_style_one(self):
        """
            样式一
        """
        rid = 'Toool090'
        # 文字
        default_text = {
            'sale_price': '￥%s' % self.data.get('sale_price'),
            'hint_text': '长按识别小程序码'
        }

        goods_title_data = format_text_data(self.data, TextType.Title, 38, None, 'left', '#333333', 50, 780, 0)
        goods_price_data = format_text_data(default_text, TextType.SalePrice, 38, None, 'left', '#DD3C3C', 50, 906, 1)
        hint_text_data = format_text_data(default_text, TextType.Hint, 28, None, 'left', '#666666', 50, 1094, 2)
        brand_name_data = format_text_data(self.data, TextType.BrandName, 28, None, 'left', '#999999', 160, 1184, 3)

        texts = [goods_title_data, goods_price_data, hint_text_data, brand_name_data]

        # 图片
        goods_image_data = format_image_data(self.data, ImageType.Goods, 750, 750, 0, 0, 0)
        wxa_code_image_data = format_image_data(self.data, ImageType.Wxacode, 250, 250, 450, 1044, 1)
        logo_image_data = format_image_data(self.data, ImageType.Logo, 80, 80, 50, 1164, 2)

        images = [goods_image_data, wxa_code_image_data, logo_image_data]

        # 图形元素
        draw_line_data = format_shape_data(DrawShapeType.Line, [(50, 990), (700, 990)], 1, '#979797', 0)

        shapes = [draw_line_data]

        # 格式化数据
        return format_style_data(self.style_id, self.size, self.color, texts, images, shapes)

    def get_style_two(self):
        """
            样式二
        """

        default_text = {
            'sale_price': '￥%s' % self.data.get('sale_price'),
            'hint_text': '长按识别小程序码'
        }

        goods_title_data = format_text_data(self.data, TextType.Title, 37, None, 'left', '#333333', 50, 520, 0)
        goods_price_data = format_text_data(default_text, TextType.SalePrice, 37, None, 'left', '#DD3C3C', 50, 646, 1)
        hint_text_data = format_text_data(default_text, TextType.Hint, 28, None, 'left', '#999999', 50, 905, 2)
        brand_name_data = format_text_data(self.data, TextType.BrandName, 28, None, 'left', '#666666', 160, 985, 3)

        texts = [goods_title_data, goods_price_data, hint_text_data, brand_name_data]

        # 图片
        goods_image_data = format_image_data(self.data, ImageType.Goods, 650, 420, 50, 50, 0)
        qr_code_image_data = format_image_data(self.data, ImageType.QRCode, 160, 160, 540, 890, 1)
        logo_image_data = format_image_data(self.data, ImageType.Logo, 80, 80, 50, 965, 2)

        images = [goods_image_data, qr_code_image_data, logo_image_data]

        # 图形元素
        draw_line_data = format_shape_data(DrawShapeType.Line, [(50, 839), (700, 839)], 1, '#979797', 0)

        shapes = [draw_line_data]

        # 格式化数据
        width, height = 750, 1101
        size = {"width": width, "height": height}

        return format_style_data(self.style_id, size, self.color, texts, images, shapes)

    def get_style_data(self):
        """
        获取海报样式数据

        :return: 样式数据
        """

        style_id = str(self.style_id)

        style_data = self.styles.get(style_id)

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
        width, height = Size.POSTER_IMAGE_SIZE['width'], Size.POSTER_IMAGE_SIZE['height']
        self.size = {"width": width, "height": height}
        self.color = (255, 255, 255)
        self.data = post_data or {}

        # 样式id参数绑定的数据方法
        self.styles = {'1': self.get_style_one(),
                       '2': self.get_style_two(),
                       '3': self.get_style_three(),
                       '4': self.get_style_four(),
                       '5': self.get_style_five()}

    def get_style_one(self):
        """
            样式一
        """

        text_color = '#FFFFFF'

        # 文字
        default_text = {
            'sales_pct': '%s折' % self.data.get('sales_pct'),
            'sales_brand': '店铺名：%s' % self.data.get('sales_brand')
        }

        sales_title_data = format_text_data(self.data, TextType.SalesTitle, 42, None, 'center', text_color, 194, 123, 0)
        sales_pct_data = format_text_data(default_text, TextType.SalesPCT, 190, 'PingFang Bold', 'center', text_color, 225, 146, 1)
        sales_info_data = format_text_data(self.data, TextType.SalesInfo, 90, None, 'center', text_color, 196, 357, 2)
        sales_brand_data = format_text_data(default_text, TextType.SalesBrand, 30, None, 'center', '#333333', 215, 564, 3)
        time_data = format_text_data(self.data, TextType.Time, 30, None, 'center', text_color, 283, 473, 4)

        texts = [sales_title_data, sales_pct_data, sales_info_data, sales_brand_data, time_data]

        # 图片
        background_image_data = format_image_data(self.data, ImageType.Background, 750, 750, 0, 0, 0)

        images = [background_image_data]

        # 图形元素
        draw_rectangle_data = format_shape_data(DrawShapeType.Rectangle, [(193, 545), (553, 625)], 1, '#FFFFFF', None, 0)

        shapes = [draw_rectangle_data]

        # 格式化数据
        width, height = 750, 750
        size = {"width": width, "height": height}
        return format_style_data(self.style_id, size, self.color, texts, images, shapes)

    def get_style_two(self):
        """
            样式二
        """

        text_color = '#FFFFFF'

        # 文字
        default_text = {
            'sales_pct': '%s折' % self.data.get('sales_pct'),
            'sales_brand': '店铺名：%s' % self.data.get('sales_brand')
        }

        sales_title_data = format_text_data(self.data, TextType.SalesTitle, 42, None, 'center', text_color, 194, 123, 0)
        sales_pct_data = format_text_data(default_text, TextType.SalesPCT, 190, 'PingFang Bold', 'center', text_color, 225, 146, 1)
        sales_info_data = format_text_data(self.data, TextType.SalesInfo, 90, None, 'center', text_color, 196, 357, 2)
        sales_brand_data = format_text_data(default_text, TextType.SalesBrand, 30, None, 'center', '#333333', 215, 564, 3)
        time_data = format_text_data(self.data, TextType.Time, 30, None, 'center', text_color, 283, 473, 4)
        hint_text = format_text_data(self.data, TextType.Hint, 24, 'PingFang Light', 'center', '#333333', 260, 1080, 5)

        texts = [sales_title_data, sales_pct_data, sales_info_data, sales_brand_data, time_data, hint_text]

        # 图片
        background_image_data = format_image_data(self.data, ImageType.Background, 750, 750, 0, 0, 0)
        qr_code_image_data = format_image_data(self.data, ImageType.QRCode, 250, 250, 250, 810, 1)

        images = [background_image_data, qr_code_image_data]

        # 图形元素
        draw_rectangle_data = format_shape_data(DrawShapeType.Rectangle, [(193, 545), (553, 625)], 1, '#FFFFFF', None, 0)

        shapes = [draw_rectangle_data]

        # 格式化数据
        width, height = 750, 1150
        size = {"width": width, "height": height}

        return format_style_data(self.style_id, size, self.color, texts, images, shapes)

    def get_style_three(self):
        """
            样式三
        """

        text_color = '#3A4837'

        # 文字
        default_text = {
            'other_1': '新品',
            'other_2': '特惠',
            'sales_pct': '全场 %s 折' % self.data.get('sales_pct'),
            'hint_text': '扫    码    参    加'
        }
        sales_title_data = format_text_data(self.data, TextType.SalesTitle, 30, 'PingFang Light', 'center', text_color, 240, 415, 0)
        sales_pct_data = format_text_data(default_text, TextType.SalesPCT, 22, 'PingFang Light', 'center', text_color, 414, 690, 1)
        sales_info_data = format_text_data(self.data, TextType.SalesInfo, 22, 'PingFang Light', 'center', '#FFFFFF', 240, 690, 2)
        sales_other_1 = format_text_data(default_text, TextType.OtherInfo1, 160, 'PingFang Light', 'center', text_color, 215, 207, 3)
        sales_other_2 = format_text_data(default_text, TextType.OtherInfo2, 160, 'PingFang Light', 'center', text_color, 215, 441, 4)
        hint_text = format_text_data(default_text, TextType.Hint, 24, 'PingFang Light', 'center', text_color, 279, 1143, 5)

        texts = [sales_title_data, sales_pct_data, sales_info_data, sales_other_1, sales_other_2, hint_text]

        # 图片素材
        # background_image = take_view_url(1)
        background_image = 'https://kg.erp.taihuoniao.com/image_background/20180329/cJtBGmvIrKeiqCHoQuRF.png'
        default_image = {'background_img': background_image}

        background_image_data = format_image_data(default_image, ImageType.Background, 750, 1334, 0, 0, 0)
        qr_code_image_data = format_image_data(self.data, ImageType.QRCode, 180, 180, 285, 944, 1)

        images = [background_image_data, qr_code_image_data]

        # 图形元素
        draw_rectangle_1_data = format_shape_data(DrawShapeType.Rectangle, [(225, 685), (525, 725)], None, '#3A4837', '#3A4837', 0)
        draw_rectangle_2_data = format_shape_data(DrawShapeType.Rectangle, [(391, 686), (524, 724)], None, '#FFFFFF', None, 0)
        draw_rectangle_3_data = format_shape_data(DrawShapeType.Rectangle, [(275, 935), (475, 1134)], None, None, '#3A4837', 0)

        shapes = [draw_rectangle_1_data, draw_rectangle_2_data, draw_rectangle_3_data]

        # 格式化数据
        background_color = (238, 238, 230)
        return format_style_data(self.style_id, self.size, background_color, texts, images, shapes)

    def get_style_four(self):
        """
            样式四
        """

        text_color = '#F08D5D'

        # 文字
        default_text = {
            'other_1': '新·品·特·惠',
            'hint_text': '扫    码    参    加',
            'symbol_pct': '%',
            'symbol_off': 'OFF'
        }
        sales_title_data = format_text_data(self.data, TextType.SalesTitle, 30, 'PingFang Light', 'center', text_color, 240, 395, 0)
        sales_pct_data = format_text_data(self.data, TextType.SalesPCT, 360, 'DIN Condensed Bold', 'left', text_color, 213, 487, 1)
        sales_info_data = format_text_data(self.data, TextType.SalesInfo, 24, 'PingFang Light', 'center', text_color, 203, 803, 2)
        sales_other_1 = format_text_data(default_text, TextType.OtherInfo1, 70, 'PingFang Light', 'center', text_color, 183, 287, 3)
        hint_text = format_text_data(default_text, TextType.Hint, 24, 'PingFang Light', 'center', text_color, 282, 1058, 4)
        symbol_pct = format_text_data(default_text, TextType.SymbolPCT, 120, 'DIN Condensed Bold', 'left', text_color, 480, 612, 5)
        symbol_off = format_text_data(default_text, TextType.SymbolOff, 48, 'DIN Condensed Bold', 'left', text_color, 480, 712, 6)

        texts = [sales_title_data, sales_pct_data, sales_info_data, sales_other_1, hint_text, symbol_pct, symbol_off]

        # 图片素材
        # background_image = take_view_url(2)
        background_image = 'https://kg.erp.taihuoniao.com/image_background/20180329/JlyhMHvKNgpeRaDULocC.png'
        default_image = {'background_img': background_image}

        background_image_data = format_image_data(default_image, ImageType.Background, 691, 1200, 30, 87, 0)
        qr_code_image_data = format_image_data(self.data, ImageType.QRCode, 140, 140, 305, 882, 1)

        images = [background_image_data, qr_code_image_data]

        # 图形元素
        draw_rectangle_1_data = format_shape_data(DrawShapeType.Rectangle, [(295, 872), (455, 1032)], None, None, '#F08D5D', 0)

        shapes = [draw_rectangle_1_data]

        # 格式化数据
        return format_style_data(self.style_id, self.size, self.color, texts, images, shapes)

    def get_style_five(self):
        """
            样式五
        """

        text_color = '#FD4136'

        # 文字
        default_text = {
            'other_1': '春 季 特 惠',
            'hint_text': '扫   码   参   加',
            'sales_pct': '全 场 %s  折' % self.data.get('sales_pct')
        }
        sales_title_data = format_text_data(self.data, TextType.SalesTitle, 200, 'DIN Condensed Bold', 'left', text_color, 139, 160, 0)
        sales_other_1 = format_text_data(default_text, TextType.OtherInfo1, 90, 'PingFang Regular', 'center', text_color, 150, 350, 1)
        sales_pct_data = format_text_data(default_text, TextType.SalesPCT, 90, 'PingFang Regular', 'center', text_color, 153, 490, 2)
        time_data = format_text_data(self.data, TextType.Time, 40, 'DIN Condensed Bold', 'center', '#FFFFFF', 233, 690, 3)
        sales_info_data = format_text_data(self.data, TextType.SalesInfo, 24, 'PingFang Regular', 'center', text_color, 203, 962, 4)
        hint_text = format_text_data(default_text, TextType.Hint, 24, 'PingFang Light', 'center', '#000000', 291, 1241, 5)

        texts = [sales_title_data, sales_other_1, sales_pct_data, time_data, sales_info_data, hint_text]

        # 图片素材
        # background_image = take_view_url(2)
        background_image = 'https://kg.erp.taihuoniao.com/image_background/20180329/tZdUMRjGCHlhbrSeAWiE.png'
        default_image = {'background_img': background_image}

        background_image_data = format_image_data(default_image, ImageType.Background, 750, 750, 0, 0, 0)
        qr_code_image_data = format_image_data(self.data, ImageType.QRCode, 200, 200, 275, 1031, 1)

        images = [background_image_data, qr_code_image_data]

        # 图形元素
        draw_rectangle_1_data = format_shape_data(DrawShapeType.Rectangle, [(0, 1294), (750, 1334)], None, '#FD4136', None, 0)

        shapes = [draw_rectangle_1_data]

        # 格式化数据
        return format_style_data(self.style_id, self.size, self.color, texts, images, shapes)

    def get_style_data(self):
        """
        获取海报样式数据

        :return: 样式数据
        """

        style_id = str(self.style_id)

        style_data = self.styles.get(style_id)

        return style_data
