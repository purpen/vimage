# -*- coding: utf-8 -*-
from vimage.helpers.poster_style_format import *
from vimage.constant import *
from vimage.models.asset import *
from vimage.helpers.image_tools import *


def take_view_url(asset_id):
    """
    从数据库获取图片素材链接

    :param asset_id: 查询主键
    :return: 图片链接
    """

    asset = Asset.query.filter_by(id=asset_id).first()
    image_url = asset.view_url if asset else ''

    return image_url


class GoodsWxaStyle:
    """
        商品小程序分享样式
    """

    def __init__(self, post_data, style_id=1):
        """
        初始化样式

        :param post_data: 海报数据
        :param style_id: 选择的样式
        """

        self.data = post_data or {}

        self.goods_images = self.data.get('goods_images')[:4]
        self.width = Size.POSTER_IMAGE_SIZE['width']   # 海报宽度不变，高度随着商品图片数量改变，(w, h)
        self.footer_h = 280
        self.center_h = 280
        self.color = (255, 255, 255)
        self.size = self.get_canvas_size()

        # 样式id参数绑定的数据方法
        self.style_id = style_id
        self.styles = {'1': self.get_style_one()}

    def get_canvas_size(self):
        """
            获取商品图片的比例
        """

        width = self.width

        # 正方形样式的尺寸
        square_size = {
            '1': (width, 1334),
            '2': (width, 1960),
            '3': (width, 1614),
            '4': (width, 1500)
        }

        # 矩形样式的尺寸
        rectangle_size = {
            '1': (width, 1100),
            '2': (width, 1500),
            '3': (width, 1270),
            '4': (width, 1730)
        }

        # 根据图片比例设置画布大小
        is_square = self.images_is_square()  # 是否加载正方形图片布局
        style_size = square_size if is_square else rectangle_size  # 选择样式尺寸
        canvas_size = style_size.get(str(len(self.goods_images)), '1')  # 设置海报的尺寸

        return canvas_size

    def images_is_square(self):
        """
            图片是否为正方形
        """

        # 加载图片，计算图片比例
        first_image = load_url_image(self.goods_images[0])
        img_width, img_height = first_image.size

        # 是否加载正方形图片布局
        is_square = True if img_width / img_height == 1 else False

        return is_square

    def s_goods_images_view(self):
        """
            正方形图片内容视图
        """

        img_count = len(self.goods_images)  # 图片数量
        f_img_w = 750  # 全屏图片宽度
        i_img_w = 670  # 有间隔图片宽度

        # 图片样式集合
        images_style_data = []

        if img_count == 1:
            # 全屏状态的图片，第一张
            full_image_data = format_image_data(post_data=self.data, url=self.goods_images[0], path=None, image_type=ImageType.Goods,
                                                width=f_img_w, height=f_img_w, radius=0, x=0, y=0, z_index=0)

            images_style_data.append(full_image_data)

        else:
            # 有间隔状态的图片，第一张
            interval_image_data = format_image_data(post_data=self.data, url=self.goods_images[0], path=None, image_type=ImageType.Goods,
                                                    width=i_img_w, height=i_img_w, radius=0, x=40, y=40, z_index=0)

            images_style_data.append(interval_image_data)

            width = (i_img_w - 20 * (img_count - 2)) / (img_count - 1)  # 附加图片的宽度

            for index in range(len(self.goods_images[1:])):
                img_url = self.goods_images[1:][index]  # 图片地址
                image_x = 40 + (width + 20) * index  # 附加图片的x间隔
                goods_image_data = format_image_data(post_data=self.data, url=img_url, path=None, image_type=ImageType.Goods,
                                                     width=width, height=width, radius=0, x=image_x, y=i_img_w + 60,
                                                     z_index=index + 1)

                images_style_data.append(goods_image_data)

        # 视图尺寸
        size = (self.size[0], self.size[1] - self.center_h - self.footer_h)

        return {
            'size': size,
            'texts': [],
            'images': images_style_data,
            'shapes': []
        }

    def r_goods_images_view(self):
        """
            矩形形图片内容视图
        """

        img_w = 670  # 默认图片宽度
        img_h = 440  # 默认图片高度
        min_w = (img_w - 20) / 2  # 图片的最小宽度
        min_h = min_w / img_w * img_h  # 图片的最小高度

        # 图片样式集合
        images_style_data = []

        # 有间隔状态的图片，第一张
        interval_image_data = format_image_data(post_data=self.data, url=self.goods_images[0], path=None, image_type=ImageType.Goods,
                                                width=img_w, height=img_h, radius=0, x=40, y=40, z_index=0)

        images_style_data.append(interval_image_data)

        for index in range(len(self.goods_images[1:])):
            img_url = self.goods_images[index + 1]  # 图片地址

            width = img_w if index == 2 else min_w  # 图片宽度
            height = img_h if index == 2 else min_h  # 图片高度
            image_x = 40 if index != 1 else 60 + min_w  # 图片的x间隔
            image_y = 80 + image_h + img_h if index == 2 else 60 + img_h  # 图片的y间隔

            goods_image_data = format_image_data(post_data=self.data, url=img_url, path=None, image_type=ImageType.Goods,
                                                 width=width if len(self.goods_images) > 2 else img_w,
                                                 height=height if len(self.goods_images) > 2 else img_h,
                                                 radius=0, x=image_x, y=image_y, z_index=index + 1)

            images_style_data.append(goods_image_data)

        # 视图尺寸
        size = (self.size[0], self.size[1] - self.center_h - self.footer_h)

        return {
            'size': size,
            'texts': [],
            'images': images_style_data,
            'shapes': []
        }

    def center_view(self):
        """
            中部内容视图数据
        """

        size = (self.width, self.center_h)

        # 商品标题
        goods_title_data = format_text_data(post_data=self.data, text=None, text_type=TextType.Title,
                                            font_size=38, font_family=None, align='left', text_color='#333333',
                                            x=60, y=40, spacing=None, z_index=0)

        # 商品价格
        default_text = {
            'sale_price': '￥%s' % self.data.get('sale_price'),
        }
        goods_price_data = format_text_data(post_data=default_text, text=None, text_type=TextType.SalePrice,
                                            font_size=38, font_family=None, align='left', text_color='#DD3C3C',
                                            x=60, y=164, spacing=None, z_index=1)

        return {
            'size': size,
            'texts': [goods_title_data, goods_price_data],
            'images': [],
            'shapes': []
        }

    def footer_view(self):
        """
            底部内容视图数据
        """

        size = (self.width, self.footer_h)

        # 提示文字
        default_text = {
            'hint_text': '长按识别小程序码'
        }
        hint_text_data = format_text_data(post_data=default_text, text=None, text_type=TextType.Hint, font_size=28,
                                          font_family=None, align='left', text_color='#999999', x=60, y=56,
                                          spacing=None, z_index=0)

        # 品牌名称
        brand_name_data = format_text_data(post_data=self.data, text=None, text_type=TextType.BrandName, font_size=32,
                                           font_family=None, align='left', text_color='#666666', x=170, y=144,
                                           spacing=None, z_index=1)

        # 二维码
        qr_code_image_data = format_image_data(post_data=self.data, url=None, path=None, image_type=ImageType.QRCode, width=180,
                                               height=180, radius=0, x=510, y=40, z_index=0)

        # 品牌logo
        logo_image_data = format_image_data(post_data=self.data, url=None, path=None, image_type=ImageType.Logo, width=80,
                                            height=80, radius=0, x=60, y=126, z_index=1)

        # 分割线，图形元素
        draw_line_data = format_shape_data(shape_type=DrawShapeType.Line, position=[(60, 1), (690, 1)],
                                           width=1, color='#979797', out_color=None, z_index=0)

        return {
            'size': size,
            'texts': [hint_text_data, brand_name_data],
            'images': [qr_code_image_data, logo_image_data],
            'shapes': [draw_line_data]
        }

    def get_style_one(self):
        """
           样式一
        """

        # 视图数据
        goods_image_view = self.s_goods_images_view() if self.images_is_square() else self.r_goods_images_view()
        goods_info_view = self.center_view()
        footer_view = self.footer_view()

        # 视图集合
        views = [goods_image_view, goods_info_view, footer_view]

        return {
            'id': self.style_id,
            'size': self.size,
            'color': self.color,
            'views': views
        }

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
        self.size = (width, height)
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

        sales_title_data = format_text_data(post_data=self.data, text=None, text_type=TextType.SalesTitle, font_size=42,
                                            font_family=None, align='center', text_color=text_color,
                                            x=194, y=123, spacing=None, z_index=0)

        sales_pct_data = format_text_data(post_data=default_text, text=None, text_type=TextType.SalesPCT, font_size=190,
                                          font_family='PingFang Bold', align='center', text_color=text_color,
                                          x=225, y=146, spacing=None, z_index=1)

        sales_info_data = format_text_data(post_data=self.data, text=None, text_type=TextType.SalesInfo, font_size=90,
                                           font_family=None, align='center', text_color=text_color,
                                           x=196, y=357, spacing=None, z_index=2)

        sales_brand_data = format_text_data(post_data=default_text, text=None, text_type=TextType.SalesBrand, font_size=30,
                                            font_family=None, align='center', text_color='#333333',
                                            x=215, y=564, spacing=None, z_index=3)

        time_data = format_text_data(post_data=self.data, text=None, text_type=TextType.Time, font_size=30,
                                     font_family=None, align='center', text_color=text_color,
                                     x=283, y=473, spacing=None, z_index=4)

        texts = [sales_title_data, sales_pct_data, sales_info_data, sales_brand_data, time_data]

        # 图片
        background_image_data = format_image_data(post_data=self.data, url=None, path=None, image_type=ImageType.Background,
                                                  width=750, height=750, radius=0, x=0, y=0, z_index=0)

        images = [background_image_data]

        # 图形元素
        draw_rectangle_data = format_shape_data(shape_type=DrawShapeType.Rectangle, position=[(193, 545), (553, 625)],
                                                width=1, color='#FFFFFF', out_color=None, z_index=0)

        shapes = [draw_rectangle_data]

        # 格式化数据
        size = (750, 750)
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

        sales_title_data = format_text_data(post_data=self.data, text=None, text_type=TextType.SalesTitle, font_size=42,
                                            font_family=None, align='center', text_color=text_color,
                                            x=194, y=123, spacing=None, z_index=0)

        sales_pct_data = format_text_data(post_data=default_text, text=None, text_type=TextType.SalesPCT, font_size=190,
                                          font_family='PingFang Bold', align='center', text_color=text_color,
                                          x=225, y=146, spacing=None, z_index=1)

        sales_info_data = format_text_data(post_data=self.data, text=None, text_type=TextType.SalesInfo, font_size=90,
                                           font_family=None, align='center', text_color=text_color,
                                           x=196, y=357, spacing=None, z_index=2)

        sales_brand_data = format_text_data(post_data=default_text, text=None, text_type=TextType.SalesBrand, font_size=30,
                                            font_family=None, align='center', text_color='#333333',
                                            x=215, y=564, spacing=None, z_index=3)

        time_data = format_text_data(post_data=self.data, text=None, text_type=TextType.Time, font_size=30,
                                     font_family=None, align='center', text_color=text_color,
                                     x=283, y=473, spacing=None, z_index=4)

        hint_text = format_text_data(post_data=self.data, text=None, text_type=TextType.Hint, font_size=24,
                                     font_family='PingFang Light', align='center', text_color='#333333',
                                     x=260, y=1080, spacing=None, z_index=5)

        texts = [sales_title_data, sales_pct_data, sales_info_data, sales_brand_data, time_data, hint_text]

        # 图片
        background_image_data = format_image_data(post_data=self.data, url=None, path=None, image_type=ImageType.Background,
                                                  width=750, height=750, radius=0, x=0, y=0, z_index=0)

        qr_code_image_data = format_image_data(post_data=self.data, url=None, path=None, image_type=ImageType.QRCode,
                                               width=250, height=250, radius=0, x=250, y=810, z_index=1)

        images = [background_image_data, qr_code_image_data]

        # 图形元素
        draw_rectangle_data = format_shape_data(shape_type=DrawShapeType.Rectangle, position=[(193, 545), (553, 625)],
                                                width=1, color='#FFFFFF', out_color=None, z_index=0)

        shapes = [draw_rectangle_data]

        # 格式化数据
        size = (750, 1150)
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
        sales_title_data = format_text_data(post_data=self.data, text=None, text_type=TextType.SalesTitle, font_size=30,
                                            font_family='PingFang Light', align='center', text_color=text_color,
                                            x=240, y=415, spacing=None, z_index=0)

        sales_pct_data = format_text_data(post_data=default_text, text=None, text_type=TextType.SalesPCT, font_size=22,
                                          font_family='PingFang Light', align='center', text_color=text_color,
                                          x=414, y=690, spacing=None, z_index=1)

        sales_info_data = format_text_data(post_data=self.data, text=None, text_type=TextType.SalesInfo, font_size=22,
                                           font_family='PingFang Light', align='center', text_color='#FFFFFF',
                                           x=240, y=690, spacing=None, z_index=2)

        sales_other_1 = format_text_data(post_data=default_text, text=None, text_type=TextType.OtherInfo1, font_size=160,
                                         font_family='PingFang Light', align='center', text_color=text_color,
                                         x=215, y=207, spacing=None, z_index=3)

        sales_other_2 = format_text_data(post_data=default_text, text=None, text_type=TextType.OtherInfo2, font_size=160,
                                         font_family='PingFang Light', align='center', text_color=text_color,
                                         x=215, y=441, spacing=None, z_index=4)

        hint_text = format_text_data(post_data=default_text, text=None, text_type=TextType.Hint, font_size=24,
                                     font_family='PingFang Light', align='center', text_color=text_color,
                                     x=279, y=1143, spacing=None, z_index=5)

        texts = [sales_title_data, sales_pct_data, sales_info_data, sales_other_1, sales_other_2, hint_text]

        # 图片素材
        # background_image = take_view_url(1)
        background_image = 'https://kg.erp.taihuoniao.com/image_background/20180329/cJtBGmvIrKeiqCHoQuRF.png'
        default_image = {'background_img': background_image}

        background_image_data = format_image_data(post_data=default_image, url=None, path=None, image_type=ImageType.Background,
                                                  width=750, height=1334, radius=0, x=0, y=0, z_index=0)

        qr_code_image_data = format_image_data(post_data=self.data, url=None, path=None, image_type=ImageType.QRCode,
                                               width=180, height=180, radius=0, x=285, y=944, z_index=1)

        images = [background_image_data, qr_code_image_data]

        # 图形元素
        draw_rectangle_1_data = format_shape_data(shape_type=DrawShapeType.Rectangle, position=[(225, 685), (525, 725)],
                                                  width=None, color='#3A4837', out_color='#3A4837', z_index=0)

        draw_rectangle_2_data = format_shape_data(shape_type=DrawShapeType.Rectangle, position=[(391, 686), (524, 724)],
                                                  width=None, color='#FFFFFF', out_color=None, z_index=0)

        draw_rectangle_3_data = format_shape_data(shape_type=DrawShapeType.Rectangle, position=[(275, 935), (475, 1134)],
                                                  width=None, color=None, out_color='#3A4837', z_index=0)

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
        sales_title_data = format_text_data(post_data=self.data, text=None, text_type=TextType.SalesTitle, font_size=30,
                                            font_family='PingFang Light', align='center', text_color=text_color,
                                            x=240, y=395, spacing=None, z_index=0)

        sales_pct_data = format_text_data(post_data=self.data, text=None, text_type=TextType.SalesPCT, font_size=360,
                                          font_family='DIN Condensed Bold', align='left', text_color=text_color,
                                          x=213, y=487, spacing=None, z_index=1)

        sales_info_data = format_text_data(post_data=self.data, text=None, text_type=TextType.SalesInfo, font_size=24,
                                           font_family='PingFang Light', align='center', text_color=text_color,
                                           x=203, y=803, spacing=None, z_index=2)

        sales_other_1 = format_text_data(post_data=default_text, text=None, text_type=TextType.OtherInfo1, font_size=70,
                                         font_family='PingFang Light', align='center', text_color=text_color,
                                         x=183, y=287, spacing=None, z_index=3)

        hint_text = format_text_data(post_data=default_text, text=None, text_type=TextType.Hint, font_size=24,
                                     font_family='PingFang Light', align='center', text_color=text_color,
                                     x=282, y=1058, spacing=None, z_index=4)

        symbol_pct = format_text_data(post_data=default_text, text=None, text_type=TextType.SymbolPCT, font_size=120,
                                      font_family='DIN Condensed Bold', align='left', text_color=text_color,
                                      x=480, y=612, spacing=None, z_index=5)

        symbol_off = format_text_data(post_data=default_text, text=None, text_type=TextType.SymbolOff, font_size=48,
                                      font_family='DIN Condensed Bold', align='left', text_color=text_color,
                                      x=480, y=712, spacing=None, z_index=6)

        texts = [sales_title_data, sales_pct_data, sales_info_data, sales_other_1, hint_text, symbol_pct, symbol_off]

        # 图片素材
        # background_image = take_view_url(2)
        background_image = 'https://kg.erp.taihuoniao.com/image_background/20180329/JlyhMHvKNgpeRaDULocC.png'
        default_image = {'background_img': background_image}

        background_image_data = format_image_data(post_data=default_image, url=None, path=None, image_type=ImageType.Background,
                                                  width=691, height=1200, radius=0, x=30, y=87, z_index=0)

        qr_code_image_data = format_image_data(post_data=self.data, url=None, path=None, image_type=ImageType.QRCode,
                                               width=140, height=140, radius=0, x=305, y=882, z_index=1)

        images = [background_image_data, qr_code_image_data]

        # 图形元素
        draw_rectangle_1_data = format_shape_data(shape_type=DrawShapeType.Rectangle, position=[(295, 872), (455, 1032)],
                                                  width=None, color=None, out_color='#F08D5D', z_index=0)

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
        sales_title_data = format_text_data(post_data=self.data, text=None, text_type=TextType.SalesTitle, font_size=200,
                                            font_family='DIN Condensed Bold', align='left', text_color=text_color,
                                            x=139, y=160, spacing=None, z_index=0)

        sales_other_1 = format_text_data(post_data=default_text, text=None, text_type=TextType.OtherInfo1, font_size=90,
                                         font_family='PingFang Regular', align='center', text_color=text_color,
                                         x=150, y=350, spacing=None, z_index=1)

        sales_pct_data = format_text_data(post_data=default_text, text=None, text_type=TextType.SalesPCT, font_size=90,
                                          font_family='PingFang Regular', align='center', text_color=text_color,
                                          x=153, y=490, spacing=None, z_index=2)

        time_data = format_text_data(post_data=self.data, text=None, text_type=TextType.Time, font_size=40,
                                     font_family='DIN Condensed Bold', align='center', text_color='#FFFFFF',
                                     x=233, y=690, spacing=None, z_index=3)

        sales_info_data = format_text_data(post_data=self.data, text=None, text_type=TextType.SalesInfo, font_size=24,
                                           font_family='PingFang Regular', align='center', text_color=text_color,
                                           x=203, y=962, spacing=None, z_index=4)

        hint_text = format_text_data(post_data=default_text, text=None, text_type=TextType.Hint, font_size=24,
                                     font_family='PingFang Light', align='center', text_color='#000000',
                                     x=291, y=1241, spacing=None, z_index=5)

        texts = [sales_title_data, sales_other_1, sales_pct_data, time_data, sales_info_data, hint_text]

        # 图片素材
        # background_image = take_view_url(2)
        background_image = 'https://kg.erp.taihuoniao.com/image_background/20180329/tZdUMRjGCHlhbrSeAWiE.png'
        default_image = {'background_img': background_image}

        background_image_data = format_image_data(post_data=default_image, url=None, path=None, image_type=ImageType.Background,
                                                  width=750, height=750, radius=0, x=0, y=0, z_index=0)

        qr_code_image_data = format_image_data(post_data=self.data, url=None, path=None, image_type=ImageType.QRCode,
                                               width=200, height=200, radius=0, x=275, y=1031, z_index=1)

        images = [background_image_data, qr_code_image_data]

        # 图形元素
        draw_rectangle_1_data = format_shape_data(shape_type=DrawShapeType.Rectangle, position=[(0, 1294), (750, 1334)],
                                                  width=None, color='#FD4136', out_color=None, z_index=0)

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


class SayingStyle:
    """
        语录、日签样式
    """

    def __init__(self, post_data):
        """
        初始化海报样式

        :param post_data: 内容数据
        """

        self.data = post_data or {}

        self.style_id = self.data.get('style_id', '1')  # 样式id
        self.back_img = self.data.get('back_img')  # 背景图片
        self.avatar = self.data.get('avatar')  # 用户头像
        self.nickname = self.data.get('nickname')  # 用户昵称
        self.content = self.data.get('info')  # 内容文字
        self.qr_code = self.data.get('qr_code')  # 二维码图片
        self.hint_text = self.data.get('hint_text')  # 提示文字

        # 海报通用默认信息
        width, height = Size.POSTER_IMAGE_SIZE['width'], Size.POSTER_IMAGE_SIZE['height']
        self.size = (width, height)
        self.color = (255, 255, 255)

        self.styles = {
            '1': self.get_style_1()
        }

    def get_style_1(self):
        """
            样式1
        """

        # 文字
        content_data = format_text_data(post_data=self.data, text=self.content, text_type=TextType.Info, font_size=28,
                                        font_family='PingFang Regular', align='center', text_color='#333333',
                                        x=100, y=700, spacing=None, z_index=0)

        time_data = format_text_data(post_data=self.data, text='2018.05.11', text_type=TextType.Time, font_size=24,
                                     font_family='PingFang Bold', align='center', text_color='#666666',
                                     x=313, y=920, spacing=None, z_index=1)

        texts = [content_data, time_data]

        # 图片素材
        background_image_data = format_image_data(post_data=self.data, url=self.back_img, path=None, image_type=ImageType.Background,
                                                  width=750, height=480, radius=0, x=0, y=0, z_index=0)

        avatar_image_data = format_image_data(post_data=self.data, url=self.avatar, path=None, image_type=ImageType.Avatar,
                                              width=160, height=160, radius=0, x=296, y=400, z_index=1)

        qr_code_image_data = format_image_data(post_data=self.data, url=self.qr_code, path=None, image_type=ImageType.QRCode,
                                               width=160, height=160, radius=0, x=296, y=1114, z_index=2)

        images = [background_image_data, avatar_image_data, qr_code_image_data]

        # 图形元素
        draw_line_data_1 = format_shape_data(shape_type=DrawShapeType.Line, position=[(154, 938), (274, 938)],
                                             width=1, color='#979797', out_color=None, z_index=0)

        draw_line_data_2 = format_shape_data(shape_type=DrawShapeType.Line, position=[(476, 938), (596, 938)],
                                             width=1, color='#979797', out_color=None, z_index=1)

        shapes = [draw_line_data_1, draw_line_data_2]

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


class BlurryPictureStyle:
    """
        模糊图片的样式
    """

    def __init__(self, post_data):
        """
        初始化海报样式

        :param post_data: 内容数据
        """

        self.data = post_data or {}

        self.img_url = self.data.get('image_url')  # 图片 URL
        self.img_w = self.data.get('image_width', '525')  # 前端图片宽度
        self.img_h = self.data.get('image_height', '360')  # 前端图片高度
        self.w = self.data.get('width')  # 模糊区域宽度
        self.h = self.data.get('height')  # 模糊区域高度
        self.x = self.data.get('left')  # 模糊区域左边距
        self.y = self.data.get('top')  # 模糊区域顶部边距

        # 图片默认信息
        self.scale = 2
        self.size = (int(self.img_w) * self.scale, int(self.img_h) * self.scale)
        self.color = (255, 255, 255)

    def get_default_style(self):
        """
            默认样式
        """

        # 主图片
        main_image_data = format_image_data(post_data=self.data, url=self.img_url, path=None, image_type=ImageType.Background,
                                            width=int(self.img_w) * self.scale, height=int(self.img_h) * self.scale,
                                            radius=0, x=0, y=0, z_index=0)

        # 模糊贴图素材
        modify_image_data = format_image_data(post_data=self.data, url=get_random_modify_images(), path=None,
                                              image_type=ImageType.Modify,
                                              width=int(self.w) * self.scale, height=int(self.h) * self.scale,
                                              radius=0, x=int(self.x) * self.scale, y=int(self.y) * self.scale, z_index=1)

        images = [main_image_data, modify_image_data]

        # 格式化数据
        return format_style_data('1', self.size, self.color, [], images, [])


def get_random_modify_images():
    """
        随机获取修饰图片素材
    """

    images = ['http://abali.ru/wp-content/uploads/2014/01/krov_na_stene.png',
              'http://pic.90sjimg.com/design/00/77/32/90/58da1e7d710b0.png',
              'http://pic.90sjimg.com/design/00/59/79/86/590692c73531f.png',
              'http://pic16.nipic.com/20110810/8131234_121231612148_2.png',
              'http://pic30.nipic.com/20130615/11171147_053116480199_2.png',
              'http://pic36.nipic.com/20131123/6608733_190033435000_2.png']

    # return random.choice(images)
    return images[-1]


class WatermarkPictureStyle:
    """
        图片添加水印的样式
    """

    def __init__(self, post_data):
        """
        初始化海报样式

        :param post_data: 内容数据
        """

        self.data = post_data or {}

        self.img_url = self.data.get('image_url')  # 图片 URL
        self.color = (255, 255, 255)

    def get_default_style(self):
        """
            默认样式
        """

        load_image = load_url_image(self.img_url, True)
        img_w, img_h = load_image.size

        # 主图片
        main_image_data = format_image_data(post_data=self.data, url=self.img_url, path=None,
                                            image_type=ImageType.Background,
                                            width=img_w, height=img_h, radius=0, x=0, y=0, z_index=0)

        # 水印素材
        modify_image = '../vimage/vimage/resource/material/material_watermark.png'
        modify_image_data = format_image_data(post_data=None, url=None, path=modify_image,
                                              image_type=ImageType.Modify,
                                              width=img_w, height=img_h, radius=0, x=0, y=0, z_index=1)

        images = [main_image_data, modify_image_data]

        # 格式化数据
        return format_style_data('1', [int(img_w), int(img_h)], self.color, [], images, [])