# -*- coding: utf-8 -*-
from vimage.helpers.poster_style_format import *
from vimage.constant import *


class LexiPosterStyle:
    """
        lexi 平台海报
    """

    def __init__(self, post_data):
        """
        初始化海报数据

        :param post_data: 接收数据
        :param type: 海报类型
        """

        self.data = post_data or {}
        self.type = self.data.get('type') or 1

    def get_style_data(self):
        """
        获取海报样式数据

        :return: 样式数据
        """

        style_data = {
            '1': BrandPosterStyle(self.data).get_style_data(),
            '2': LifePosterStyle(self.data).get_style_data(),
            '3': WxaGoodsPosterStyle(self.data).get_style_data(),
            '4': PaaSGoodsPosterStyle(self.data).get_style_data()
        }

        type = str(self.type)
        data = style_data.get(type)

        return data


class BrandPosterStyle:
    """
        品牌馆海报分享样式
    """

    def __init__(self, post_data):
        """
        初始化样式

        :param post_data: 海报数据
        """

        self.data = post_data or {}

        self.goods_images = self.data.get('goods_images')
        self.width = Size.POSTER_IMAGE_SIZE['width']
        self.height = Size.POSTER_IMAGE_SIZE['height']
        self.color = (255, 255, 255)
        self.footer_h = 330
        self.top_h = 354
        self.size = (self.width, self.height)

    @property
    def goods_images_view(self):
        """
            正方形图片内容视图
        """

        img_count = len(self.goods_images)  # 图片数量
        a_img_w = 650  # 单图宽度
        m_img_w = 320  # 多图宽度

        # 图片样式集合
        images_style_data = []

        if 1 <= img_count < 4:
            # 只展示一张图片
            a_image_data = format_image_data(post_data=self.data, url=self.goods_images[0], image_type=ImageType.Goods,
                                             width=a_img_w, height=a_img_w, radius=8, x=50, y=0, z_index=0)

            images_style_data.append(a_image_data)

        elif img_count >= 4:
            # 多张图片 只展示4张
            for index in range(len(self.goods_images[:4])):
                img_url = self.goods_images[index]  # 图片地址

                image_x = 50 if index % 2 != 0 else m_img_w + 60  # 图片的x间隔
                image_y = 0 if index < 2 else m_img_w + 10  # 图片的y间隔
                goods_image_data = format_image_data(post_data=self.data, url=img_url, image_type=ImageType.Goods,
                                                     width=m_img_w, height=m_img_w, radius=8, x=image_x, y=image_y,
                                                     z_index=index + 1)

                images_style_data.append(goods_image_data)

        # 视图尺寸
        size = (self.width, self.height - self.top_h - self.footer_h)

        return {
            'size': size,
            'texts': [],
            'images': images_style_data,
            'shapes': []
        }

    def top_view(self):
        """
            顶部内容视图数据
        """

        size = (self.width, self.top_h)

        # 品牌logo
        brand_logo_image_data = format_image_data(post_data=self.data, url=None, image_type=ImageType.BrandLogo,
                                                  width=70, height=70, radius=8, x=50, y=50, z_index=0)

        # 描述文字背景
        background_image = {'background_img': 'https://kg.erp.taihuoniao.com/banmen/static/background_1.png'}
        default_background_data = format_image_data(post_data=background_image, url=None, image_type=ImageType.Background,
                                                    width=650, height=164, radius=0, x=50, y=150, z_index=1)

        # 提示文字
        hint_text_data = format_text_data(post_data=self.data, text='原创品牌设计馆', text_type=TextType.Info,
                                          font_size=24, font_family=None, align='left', text_color='#999999',
                                          x=140, y=50, spacing=None, z_index=0)

        # 品牌名称
        brand_name_data = format_text_data(post_data=self.data, text=None, text_type=TextType.BrandName,
                                           font_size=28, font_family='PingFang Bold', align='left',
                                           text_color='#333333', x=140, y=86, spacing=None, z_index=1)

        # 描述文字
        describe_data = {'describe': self.data.get('describe')[:69]}
        describe_text_data = format_text_data(post_data=describe_data, text=None, text_type=TextType.Describe,
                                              font_size=26, font_family=None, align='left',
                                              text_color='#333333', x=70, y=180, spacing=38, z_index=2, width=610)

        return {
            'size': size,
            'texts': [brand_name_data, hint_text_data, describe_text_data],
            'images': [brand_logo_image_data, default_background_data],
            'shapes': []
        }

    def footer_view(self):
        """
            底部内容视图数据
        """

        size = (self.width, self.footer_h)

        # 小程序码
        wxa_code_image_data = format_image_data(post_data=self.data, url=None, image_type=ImageType.WxaCode, width=180,
                                                height=180, radius=0, x=520, y=45, z_index=0)

        # 默认logo
        default_image = {'logo_img': 'https://kg.erp.taihuoniao.com/banmen/static/lexi_logo.png'}
        default_logo_data = format_image_data(post_data=default_image, url=None, image_type=ImageType.Logo, width=71,
                                              height=79, radius=0,  x=50, y=190, z_index=1)

        # 默认名称
        default_name_data = format_text_data(post_data=self.data, text='乐喜', text_type=TextType.Info,
                                             font_size=36, font_family='PingFang Bold', align='left',
                                             text_color='#666666', x=140, y=190, spacing=None, z_index=0)

        # 默认标语
        default_slogan_data = format_text_data(post_data=self.data, text='全球原创设计品位购物平台', text_type=TextType.Info,
                                               font_size=20, font_family='PingFang Bold', align='left',
                                               text_color='#666666', x=140, y=242, spacing=None, z_index=1)

        # 提示文字
        default_hint_data = format_text_data(post_data=self.data, text='长按识别小程序码', text_type=TextType.Info,
                                             font_size=24, font_family=None, align='left', text_color='#666666',
                                             x=509, y=245, spacing=None, z_index=2)

        return {
            'size': size,
            'texts': [default_name_data, default_slogan_data, default_hint_data],
            'images': [wxa_code_image_data, default_logo_data],
            'shapes': []
        }

    def get_style_one(self):
        """
           样式一
        """

        # 视图数据
        goods_image_view = self.goods_images_view
        top_view = self.top_view()
        footer_view = self.footer_view()

        # 视图集合
        views = [top_view, goods_image_view, footer_view]

        return {
            'size': self.size,
            'color': self.color,
            'views': views
        }

    def get_style_data(self):
        """
        获取海报样式数据

        :return: 样式数据
        """

        style_data = self.get_style_one()

        return style_data


class LifePosterStyle:
    """
        生活馆海报分享样式
    """

    def __init__(self, post_data):
        """
        初始化样式

        :param post_data: 海报数据
        """

        self.data = post_data or {}

        self.goods_images = self.data.get('goods_images')
        self.width = Size.POSTER_IMAGE_SIZE['width']
        self.height = Size.POSTER_IMAGE_SIZE['height']
        self.color = (255, 255, 255)
        self.footer_h = 170
        self.top_h = 335
        self.size = (self.width, self.height)

    @property
    def goods_images_view(self):
        """
            正方形图片内容视图
        """

        f_img_w = 650  # 首图宽度
        f_img_h = 500  # 首图高度
        m_img_w = 320  # 多图宽度

        # 图片样式集合
        images_style_data = []

        # 多张图片 只展示4张
        for index in range(len(self.goods_images[:3])):
            img_url = self.goods_images[index]  # 图片地址

            image_x = 50 if index < 2 else m_img_w + 60   # 图片的x间隔
            image_y = 0 if index == 0 else f_img_h + 10   # 图片的y间隔
            image_w = f_img_w if index == 0 else m_img_w  # 图片的宽度
            image_h = f_img_h if index == 0 else m_img_w  # 图片的高度

            goods_image_data = format_image_data(post_data=self.data, url=img_url, image_type=ImageType.Goods,
                                                 width=image_w, height=image_h, radius=8, x=image_x, y=image_y,
                                                 z_index=index + 1)

            images_style_data.append(goods_image_data)

        # 视图尺寸
        size = (self.width, self.height - self.top_h - self.footer_h)

        return {
            'size': size,
            'texts': [],
            'images': images_style_data,
            'shapes': []
        }

    def top_view(self):
        """
            顶部内容视图数据
        """

        size = (self.width, self.top_h)

        # 品牌logo
        brand_logo_image_data = format_image_data(post_data=self.data, url=None, image_type=ImageType.BrandLogo,
                                                  width=70, height=70, radius=8, x=50, y=50, z_index=0)

        # 描述文字素材
        modify_image = {'modify_img': 'https://kg.erp.taihuoniao.com/banmen/static/material_2.png'}
        default_modify_data = format_image_data(post_data=modify_image, url=None, image_type=ImageType.Modify,
                                                width=30, height=25, radius=0, x=50, y=160, z_index=1)

        # 描述文字素材
        modify_image_1 = {'modify_img': 'https://kg.erp.taihuoniao.com/banmen/static/material_3.png'}
        default_modify_data_1 = format_image_data(post_data=modify_image_1, url=None, image_type=ImageType.Modify,
                                                  width=30, height=25, radius=0, x=490, y=257, z_index=2)

        # 小程序码
        wxa_code_image_data = format_image_data(post_data=self.data, url=None, image_type=ImageType.WxaCode, width=180,
                                                height=180, radius=0, x=520, y=50, z_index=3)

        # 提示文字
        hint_text_data = format_text_data(post_data=self.data, text='乐喜生活馆', text_type=TextType.Info,
                                          font_size=24, font_family=None, align='left', text_color='#999999',
                                          x=140, y=50, spacing=None, z_index=0)

        # 品牌名称
        brand_name_data = format_text_data(post_data=self.data, text=None, text_type=TextType.BrandName,
                                           font_size=28, font_family='PingFang Bold', align='left',
                                           text_color='#333333', x=140, y=86, spacing=None, z_index=1)

        # 描述文字
        describe_data = {'describe': self.data.get('describe')[:32]}
        describe_text_data = format_text_data(post_data=describe_data, text=None, text_type=TextType.Describe,
                                              font_size=26, font_family=None, align='left', text_color='#333333',
                                              x=50, y=209, spacing=38, z_index=2, width=420)

        return {
            'size': size,
            'texts': [brand_name_data, hint_text_data, describe_text_data],
            'images': [brand_logo_image_data, default_modify_data, default_modify_data_1, wxa_code_image_data],
            'shapes': []
        }

    def footer_view(self):
        """
            底部内容视图数据
        """

        size = (self.width, self.footer_h)

        # 默认logo
        default_image = {'logo_img': 'https://kg.erp.taihuoniao.com/banmen/static/lexi_logo.png'}
        default_logo_data = format_image_data(post_data=default_image, url=None, image_type=ImageType.Logo, width=71,
                                              height=79, radius=0,  x=50, y=50, z_index=0)

        # 默认名称
        default_name_data = format_text_data(post_data=self.data, text='乐喜', text_type=TextType.Info,
                                             font_size=36, font_family='PingFang Bold', align='left',
                                             text_color='#666666', x=140, y=56, spacing=None, z_index=0)

        # 默认标语
        default_slogan_data = format_text_data(post_data=self.data, text='全球原创设计品位购物平台', text_type=TextType.Info,
                                               font_size=20, font_family='PingFang Bold', align='left',
                                               text_color='#666666', x=140, y=104, spacing=None, z_index=1)

        return {
            'size': size,
            'texts': [default_name_data, default_slogan_data],
            'images': [default_logo_data],
            'shapes': []
        }

    def get_style_one(self):
        """
           样式一
        """

        # 视图数据
        goods_image_view = self.goods_images_view
        top_view = self.top_view()
        footer_view = self.footer_view()

        # 视图集合
        views = [top_view, goods_image_view, footer_view]

        return {
            'size': self.size,
            'color': self.color,
            'views': views
        }

    def get_style_data(self):
        """
        获取海报样式数据

        :return: 样式数据
        """

        style_data = self.get_style_one()

        return style_data


class WxaGoodsPosterStyle:
    """
        独立小程序分享商品海报样式
    """

    def __init__(self, post_data):
        """
        初始化样式

        :param post_data: 海报数据
        """

        self.data = post_data or {}

        self.goods_images = self.data.get('goods_images')
        self.width = Size.POSTER_IMAGE_SIZE['width']
        self.height = Size.POSTER_IMAGE_SIZE['height']
        self.color = (255, 255, 255)
        self.footer_h = self.get_footer_view_height()
        self.top_h = 0
        self.size = (self.width, self.height)

    def get_footer_view_height(self):
        """
            获取内容视图的高度
        """

        return 834 if len(self.goods_images) >= 3 else 684

    @property
    def goods_images_view(self):
        """
            正方形图片内容视图
        """

        img_count = len(self.goods_images)  # 图片数量
        a_img_w = 750  # 单图宽度
        a_img_h = 650  # 单图高度
        f_img_w = 500  # 首图宽图
        m_img_w = 248  # 多图宽度

        # 图片样式集合
        images_style_data = []

        if 1 <= img_count < 3:
            # 只展示一张图片
            a_image_data = format_image_data(post_data=self.data, url=self.goods_images[0], image_type=ImageType.Goods,
                                             width=a_img_w, height=a_img_h, radius=0, x=0, y=0, z_index=0)

            images_style_data.append(a_image_data)

        elif img_count >= 3:
            # 多张图片 只展示3张
            for index in range(len(self.goods_images[:3])):
                img_url = self.goods_images[index]  # 图片地址

                image_x = 0 if index == 0 else f_img_w + 2  # 图片的x间隔
                image_y = 0 if index < 2 else m_img_w + 3  # 图片的y间隔
                image_w = f_img_w if index == 0 else m_img_w  # 图片的宽度

                goods_image_data = format_image_data(post_data=self.data, url=img_url, image_type=ImageType.Goods,
                                                     width=image_w, height=image_w, radius=0, x=image_x, y=image_y,
                                                     z_index=index + 1)

                images_style_data.append(goods_image_data)

        # 视图尺寸
        size = (self.width, self.height - self.top_h - self.footer_h)

        return {
            'size': size,
            'texts': [],
            'images': images_style_data,
            'shapes': []
        }

    def top_view(self):
        """
            顶部内容视图数据
        """

        size = (self.width, self.top_h)

        return {
            'size': size,
            'texts': [],
            'images': [],
            'shapes': []
        }

    def footer_view(self):
        """
            底部内容视图数据
        """

        size = (self.width, self.footer_h)

        default_origin_y = 0 if self.footer_h == 834 else 150

        # 默认logo
        default_image = {'logo_img': 'https://kg.erp.taihuoniao.com/banmen/static/lexi_logo.png'}
        default_logo_data = format_image_data(post_data=default_image, url=None, image_type=ImageType.Logo, width=71,
                                              height=79, radius=0,  x=60, y=664 - default_origin_y, z_index=1)

        # 默认名称
        default_name_data = format_text_data(post_data=self.data, text='乐喜', text_type=TextType.Info,
                                             font_size=36, font_family='PingFang Bold', align='left',
                                             text_color='#666666', x=150, y=669 - default_origin_y, spacing=None, z_index=0)

        # 默认标语
        default_slogan_data = format_text_data(post_data=self.data, text='全球原创设计品位购物平台', text_type=TextType.Info,
                                               font_size=20, font_family='PingFang Bold', align='left',
                                               text_color='#666666', x=150, y=720 - default_origin_y, spacing=None, z_index=1)

        # 用户头像
        user_Avatar_image_data = format_image_data(post_data=self.data, url=None, image_type=ImageType.Avatar,
                                                   width=70, height=70, radius=0, x=60, y=45, z_index=2)

        # 用户昵称
        default_nickname = {'nickname': ('%s  向你推荐了' % self.data.get('nickname'))}
        user_nickname_data = format_text_data(post_data=default_nickname, text=None, text_type=TextType.Nickname,
                                              font_size=28, font_family='PingFang Bold', align='left',
                                              text_color='#FFFFFF', x=150, y=60, spacing=None, z_index=2)

        # 小程序码
        wxa_code_image_data = format_image_data(post_data=self.data, url=None, image_type=ImageType.WxaCode, width=180,
                                                height=180, radius=0, x=504, y=522 - default_origin_y, z_index=3)

        # 提示文字
        hint_text_data = format_text_data(post_data=self.data, text='长按识别小程序码', text_type=TextType.Hint,
                                          font_size=24, font_family=None, align='left', text_color='#666666',
                                          x=498, y=722 - default_origin_y, spacing=None, z_index=3)

        # 商品名称
        title_data = {'title': self.data.get('title')[:20]}
        goods_title_data = format_text_data(post_data=title_data, text=None, text_type=TextType.Title,
                                            font_size=32, font_family='PingFang Bold', align='left',
                                            text_color='#333333', x=63, y=170, spacing=None, z_index=4)

        # 商品推荐语
        describe_content = self.data.get('describe')[:40]
        describe_data = {'describe': describe_content}
        goods_describe_data = format_text_data(post_data=describe_data, text=None, text_type=TextType.Describe,
                                               font_size=26, font_family=None, align='left', text_color='#333333',
                                               x=63, y=230, spacing=38, z_index=5, width=565)

        price_origin_y = 0 if len(describe_content) > 24 else 38
        not_describe_origin_y = 96 if len(self.data.get('describe')) == 0 else price_origin_y  # 没有商品推荐语时的顶部边距

        # 商品价格
        default_price = {'sale_price': ('￥%s' % self.data.get('sale_price'))}
        goods_price_data = format_text_data(post_data=default_price, text=None, text_type=TextType.SalePrice,
                                            font_size=28, font_family='PingFang Bold', align='left',
                                            text_color='#333333', x=63, y=316 - not_describe_origin_y, spacing=None,
                                            z_index=6)

        # 优惠红包提示
        coupon_hint_data = format_text_data(post_data=default_price, text='最高优惠红包可领', text_type=TextType.Info,
                                            font_size=24, font_family='PingFang Bold', align='left',
                                            text_color='#999999', x=63, y=364 - not_describe_origin_y, spacing=None,
                                            z_index=7)

        # 优惠红包金额
        coupon_amount = ('￥%s' % self.data.get('coupon_amount'))
        coupon_amount_data = format_text_data(post_data=self.data, text=coupon_amount, text_type=TextType.Info,
                                              font_size=32, font_family='PingFang Bold', align='left',
                                              text_color='#FFFFFF', x=97, y=413 - not_describe_origin_y,
                                              spacing=None, z_index=8)

        # 优惠红包天数
        coupon_days = ('%s天有效期' % self.data.get('coupon_days'))
        coupon_days_data = format_text_data(post_data=default_price, text=coupon_days, text_type=TextType.Info,
                                            font_size=20, font_family='PingFang Bold', align='left',
                                            text_color='#FFFFFF', x=91, y=454 - not_describe_origin_y,
                                            spacing=None, z_index=9)

        # 优惠红包背景
        coupon_image = {'modify_img': 'https://kg.erp.taihuoniao.com/banmen/static/ticket_background.png'}
        coupon_image_data = format_image_data(post_data=coupon_image, url=None, image_type=ImageType.Modify,
                                              width=150, height=80, radius=0, x=64, y=408 - not_describe_origin_y,
                                              z_index=4)

        # 背景
        image_url_id = 2 if self.footer_h == 834 else 3
        background_image = {'background_img': ('https://kg.erp.taihuoniao.com/banmen/static/background_%d.png' % image_url_id)}
        background_image_data = format_image_data(post_data=background_image, url=None, image_type=ImageType.Background,
                                                  width=self.width, height=self.footer_h - 10, radius=0, x=0, y=10,
                                                  z_index=0)

        images_data = [default_logo_data, user_Avatar_image_data, wxa_code_image_data, background_image_data]

        texts_data = [default_name_data, default_slogan_data, user_nickname_data, hint_text_data, goods_title_data,
                      goods_describe_data, goods_price_data]

        if int(self.data.get('coupon_amount')) > 0:
            images_data.append(coupon_image_data)
            texts_data.append(coupon_hint_data)
            texts_data.append(coupon_amount_data)
            texts_data.append(coupon_days_data)

        return {
            'size': size,
            'texts': texts_data,
            'images': images_data,
            'shapes': []
        }

    def get_style_one(self):
        """
           样式一
        """

        # 视图数据
        goods_image_view = self.goods_images_view
        top_view = self.top_view()
        footer_view = self.footer_view()

        # 视图集合
        views = [top_view, goods_image_view, footer_view]

        return {
            'size': self.size,
            'color': self.color,
            'views': views
        }

    def get_style_data(self):
        """
        获取海报样式数据

        :return: 样式数据
        """

        style_data = self.get_style_one()

        return style_data


class PaaSGoodsPosterStyle:
    """
        核心平台小程序分享商品海报样式
    """

    def __init__(self, post_data):
        """
        初始化样式

        :param post_data: 海报数据
        """

        self.data = post_data or {}

        self.goods_images = self.data.get('goods_images')
        self.width = Size.POSTER_IMAGE_SIZE['width']
        self.height = Size.POSTER_IMAGE_SIZE['height']
        self.color = (255, 255, 255)
        self.footer_h = self.get_footer_view_height()
        self.top_h = self.get_top_view_height()
        self.size = (self.width, self.height)

    def get_footer_view_height(self):
        """
            获取底部内容视图的高度
        """

        return 570 if len(self.goods_images) >= 3 else 714

    def get_top_view_height(self):
        """
            获取顶部内容视图的高度
        """

        return 260 if len(self.goods_images) >= 3 else 0

    @property
    def goods_images_view(self):
        """
            正方形图片内容视图
        """

        img_count = len(self.goods_images)  # 图片数量
        a_img_h = 650  # 单图高度
        f_img_w = 396  # 首图宽图
        f_img_h = 500  # 首图高图
        m_img_w = 246  # 多图宽度

        # 图片样式集合
        images_style_data = []

        if 1 <= img_count < 3:
            # 只展示一张图片
            a_image_data = format_image_data(post_data=self.data, url=self.goods_images[0], image_type=ImageType.Goods,
                                             width=self.width, height=a_img_h, radius=0, x=0, y=0, z_index=0)

            images_style_data.append(a_image_data)

        elif img_count >= 3:
            # 多张图片 只展示3张
            for index in range(len(self.goods_images[:3])):
                img_url = self.goods_images[index]  # 图片地址

                image_x = 50 if index == 0 else f_img_w + 58  # 图片的x间隔
                image_y = 0 if index < 2 else m_img_w + 8  # 图片的y间隔
                image_w = f_img_w if index == 0 else m_img_w  # 图片的宽度
                image_h = f_img_h if index == 0 else m_img_w  # 图片的高度

                goods_image_data = format_image_data(post_data=self.data, url=img_url, image_type=ImageType.Goods,
                                                     width=image_w, height=image_h, radius=8, x=image_x, y=image_y,
                                                     z_index=index + 1)

                images_style_data.append(goods_image_data)

        # 视图尺寸
        size = (self.width, self.height - self.top_h - self.footer_h)

        return {
            'size': size,
            'texts': [],
            'images': images_style_data,
            'shapes': []
        }

    def top_view(self):
        """
            顶部内容视图数据
        """

        size = (self.width, self.top_h)

        # 默认
        default_title_image = {'modify_img': 'https://kg.erp.taihuoniao.com/banmen/static/material_1.png'}
        default_title_data = format_image_data(post_data=default_title_image, url=None, image_type=ImageType.Modify,
                                               width=375, height=61, radius=0, x=50, y=50, z_index=0)

        # 用户头像
        user_Avatar_image_data = format_image_data(post_data=self.data, url=None, image_type=ImageType.Avatar,
                                                   width=70, height=70, radius=0, x=50, y=160, z_index=1)

        # 用户昵称
        default_nickname = {'nickname': ('%s  向你推荐了' % self.data.get('nickname'))}
        user_nickname_data = format_text_data(post_data=default_nickname, text=None, text_type=TextType.Nickname,
                                              font_size=28, font_family='PingFang Bold', align='left',
                                              text_color='#333333', x=140, y=175, spacing=None, z_index=0)

        image_count = len(self.goods_images)

        return {
            'size': size,
            'texts': [] if image_count < 3 else [user_nickname_data],
            'images': [] if image_count < 3 else [default_title_data, user_Avatar_image_data],
            'shapes': []
        }

    def footer_view(self):
        """
            底部内容视图数据
        """

        size = (self.width, self.footer_h)

        default_origin_y = 0 if self.footer_h == 570 else 144

        # 默认logo
        default_image = {'logo_img': 'https://kg.erp.taihuoniao.com/banmen/static/lexi_logo.png'}
        default_logo_data = format_image_data(post_data=default_image, url=None, image_type=ImageType.Logo, width=71,
                                              height=79, radius=0,  x=50, y=434 + default_origin_y, z_index=1)

        # 默认名称
        default_name_data = format_text_data(post_data=self.data, text='乐喜', text_type=TextType.Info,
                                             font_size=36, font_family='PingFang Bold', align='left',
                                             text_color='#666666', x=140, y=439 + default_origin_y, spacing=None, z_index=0)

        # 默认标语
        default_slogan_data = format_text_data(post_data=self.data, text='全球原创设计品位购物平台', text_type=TextType.Info,
                                               font_size=20, font_family='PingFang Bold', align='left',
                                               text_color='#666666', x=140, y=490 + default_origin_y, spacing=None, z_index=1)

        # 用户头像
        user_Avatar_image_data = format_image_data(post_data=self.data, url=None, image_type=ImageType.Avatar,
                                                   width=70, height=70, radius=0, x=70, y=45, z_index=2)

        # 用户昵称
        default_nickname = {'nickname': ('%s  向你推荐了' % self.data.get('nickname'))}
        user_nickname_data = format_text_data(post_data=default_nickname, text=None, text_type=TextType.Nickname,
                                              font_size=28, font_family='PingFang Bold', align='left',
                                              text_color='#333333', x=160, y=60, spacing=None, z_index=2)

        # 小程序码
        wxa_code_image_data = format_image_data(post_data=self.data, url=None, image_type=ImageType.WxaCode, width=180,
                                                height=180, radius=0, x=514, y=289 + default_origin_y, z_index=3)

        # 提示文字
        hint_text_data = format_text_data(post_data=self.data, text='长按识别小程序码', text_type=TextType.Hint,
                                          font_size=24, font_family=None, align='left', text_color='#666666',
                                          x=508, y=489 + default_origin_y, spacing=None, z_index=3)

        # 商品名称
        title_data = {'title': self.data.get('title')[:20]}
        goods_title_data = format_text_data(post_data=title_data, text=None, text_type=TextType.Title,
                                            font_size=32, font_family='PingFang Bold', align='left',
                                            text_color='#333333', x=50, y=37 + default_origin_y, spacing=None, z_index=4)

        # 商品推荐语
        describe_content = self.data.get('describe')[:50]
        describe_data = {'describe': describe_content}
        goods_describe_data = format_text_data(post_data=describe_data, text=None, text_type=TextType.Describe,
                                               font_size=26, font_family=None, align='left', text_color='#333333',
                                               x=50, y=90 + default_origin_y, spacing=38, z_index=5, width=650)

        price_origin_y = 0 if len(describe_content) > 24 else 38
        not_describe_origin_y = 96 if len(self.data.get('describe')) == 0 else price_origin_y  # 没有商品推荐语时的顶部边距

        # 商品价格
        default_price = {'sale_price': ('￥%s' % self.data.get('sale_price'))}
        goods_price_data = format_text_data(post_data=default_price, text=None, text_type=TextType.SalePrice,
                                            font_size=28, font_family='PingFang Bold', align='left',
                                            text_color='#333333', x=50, y=183 + default_origin_y - not_describe_origin_y,
                                            spacing=None, z_index=6)

        # 优惠红包提示
        coupon_hint_data = format_text_data(post_data=default_price, text='最高优惠红包可领', text_type=TextType.Info,
                                            font_size=24, font_family='PingFang Bold', align='left',
                                            text_color='#999999', x=50, y=231 + default_origin_y - not_describe_origin_y,
                                            spacing=None, z_index=7)

        # 优惠红包金额
        coupon_amount = ('￥%s' % self.data.get('coupon_amount'))
        coupon_amount_data = format_text_data(post_data=self.data, text=coupon_amount, text_type=TextType.Info,
                                              font_size=32, font_family='PingFang Bold', align='left',
                                              text_color='#FFFFFF', x=90, y=282 + default_origin_y - not_describe_origin_y,
                                              spacing=None, z_index=8)

        # 优惠红包天数
        coupon_days = ('%s天有效期' % self.data.get('coupon_days'))
        coupon_days_data = format_text_data(post_data=default_price, text=coupon_days, text_type=TextType.Info,
                                            font_size=20, font_family='PingFang Bold', align='left',
                                            text_color='#FFFFFF', x=78, y=322 + default_origin_y - not_describe_origin_y,
                                            spacing=None, z_index=9)

        # 优惠红包背景
        coupon_image = {'modify_img': 'https://kg.erp.taihuoniao.com/banmen/static/ticket_background.png'}
        coupon_image_data = format_image_data(post_data=coupon_image, url=None, image_type=ImageType.Modify,
                                              width=150, height=80, radius=0, x=50, y=275 + default_origin_y - not_describe_origin_y,
                                              z_index=4)

        # 背景
        background_image = {'background_img': 'https://kg.erp.taihuoniao.com/banmen/static/background_4.png'}
        background_image_data = format_image_data(post_data=background_image, url=None, image_type=ImageType.Background,
                                                  width=self.width, height=self.footer_h, radius=0, x=0, y=0, z_index=0)

        images_data = [default_logo_data, wxa_code_image_data]

        texts_data = [default_name_data, default_slogan_data, hint_text_data, goods_title_data,
                      goods_describe_data, goods_price_data]

        if self.footer_h == 714:
            images_data.append(user_Avatar_image_data)
            images_data.append(background_image_data)
            texts_data.append(user_nickname_data)

        if int(self.data.get('coupon_amount')) > 0:
            images_data.append(coupon_image_data)
            texts_data.append(coupon_hint_data)
            texts_data.append(coupon_amount_data)
            texts_data.append(coupon_days_data)

        return {
            'size': size,
            'texts': texts_data,
            'images': images_data,
            'shapes': []
        }

    def get_style_one(self):
        """
           样式一
        """

        # 视图数据
        goods_image_view = self.goods_images_view
        top_view = self.top_view()
        footer_view = self.footer_view()

        # 视图集合
        views = [top_view, goods_image_view, footer_view]

        return {
            'size': self.size,
            'color': self.color,
            'views': views
        }

    def get_style_data(self):
        """
        获取海报样式数据

        :return: 样式数据
        """

        style_data = self.get_style_one()

        return style_data