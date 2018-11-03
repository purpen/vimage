# -*- coding: utf-8 -*-
from vimage.helpers.poster_style_format import *
from vimage.constant import *
from vimage.helpers.switch import *
import random
from vimage.helpers.image_tools import *


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
        self.type = int(self.data.get('type')) or 1

    def get_style_data(self):
        """
        获取海报样式数据

        :return: 样式数据
        """

        for case in Switch(self.type):
            if case(1):
                return BrandPosterStyle(self.data).get_style_data()
            if case(2):
                return LifePosterStyle(self.data).get_style_data()
            if case(3):
                return WxaGoodsPosterStyle(self.data).get_style_data()
            if case(4):
                return PaaSGoodsPosterStyle(self.data).get_style_data()
            if case(5):
                return InviteFriendsPosterStyle(self.data).get_style_data()
            if case(6):
                return InviteFriendsCardStyle(self.data).get_style_data()
            if case(7):
                return BrandCardStyle(self.data).get_style_data()
            if case(8):
                return LifeCardStyle(self.data).get_style_data()
            if case(9):
                return PlatformCardStyle(self.data).get_style_data()
            if case(10):
                return CouponsCartStyle(self.data).get_style_data()
            if case(11):
                return GuessGamePosterStyle(self.data).get_style_first()
            if case(12):
                return GuessGamePosterStyle(self.data).get_style_second()
            if case(13):
                return GuessGamePosterStyle(self.data).get_style_third()
            if case(14):
                return GuessGamePosterStyle(self.data).get_style_fourth()
            if case(15):
                return ShopWindowPosterStyle(self.data).get_style_data()
            if case(16):
                return GoodsCardStyle(self.data).get_style_data()

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
            a_image_data = format_image_data(post_data=self.data, url=self.goods_images[0], path=None,
                                             image_type=ImageType.Goods,
                                             width=a_img_w, height=a_img_w, radius=8, x=50, y=0, z_index=0)

            images_style_data.append(a_image_data)

        elif img_count >= 4:
            # 多张图片 只展示4张
            for index in range(len(self.goods_images[:4])):
                img_url = self.goods_images[index]  # 图片地址

                image_x = 50 if index % 2 != 0 else m_img_w + 60  # 图片的x间隔
                image_y = 0 if index < 2 else m_img_w + 10  # 图片的y间隔
                goods_image_data = format_image_data(post_data=self.data, url=img_url, path=None,
                                                     image_type=ImageType.Goods,
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
        brand_logo_image_data = format_image_data(post_data=self.data, url=None, path=None,
                                                  image_type=ImageType.BrandLogo,
                                                  width=70, height=70, radius=8, x=50, y=50, z_index=0)

        # 描述文字背景
        background_image = '../vimage/vimage/resource/background/background_1.png'
        default_background_data = format_image_data(post_data=None, url=None, path=background_image,
                                                    image_type=ImageType.Background,
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
        wxa_code_image_data = format_image_data(post_data=self.data, url=None, path=None, image_type=ImageType.WxaCode,
                                                width=180,
                                                height=180, radius=0, x=520, y=45, z_index=0)

        # 默认logo
        logo_image = '../vimage/vimage/resource/material/lexi_logo.png'
        default_logo_data = format_image_data(post_data=None, url=None, path=logo_image, image_type=ImageType.Logo,
                                              width=71,
                                              height=79, radius=0, x=50, y=190, z_index=1)

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

            image_x = 50 if index < 2 else m_img_w + 60  # 图片的x间隔
            image_y = 0 if index == 0 else f_img_h + 10  # 图片的y间隔
            image_w = f_img_w if index == 0 else m_img_w  # 图片的宽度
            image_h = f_img_h if index == 0 else m_img_w  # 图片的高度

            goods_image_data = format_image_data(post_data=self.data, url=img_url, path=None,
                                                 image_type=ImageType.Goods,
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
        brand_logo_image_data = format_image_data(post_data=self.data, url=None, path=None,
                                                  image_type=ImageType.BrandLogo,
                                                  width=70, height=70, radius=8, x=50, y=50, z_index=0)

        # 描述文字素材
        modify_image = '../vimage/vimage/resource/material/material_2.png'
        default_modify_data = format_image_data(post_data=None, url=None, path=modify_image,
                                                image_type=ImageType.Modify,
                                                width=30, height=25, radius=0, x=50, y=160, z_index=1)

        # 描述文字素材
        modify_image_1 = '../vimage/vimage/resource/material/material_3.png'
        default_modify_data_1 = format_image_data(post_data=None, url=None, path=modify_image_1,
                                                  image_type=ImageType.Modify,
                                                  width=30, height=25, radius=0, x=490, y=257, z_index=2)

        # 小程序码
        wxa_code_image_data = format_image_data(post_data=self.data, url=None, path=None, image_type=ImageType.WxaCode,
                                                width=180,
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
        logo_image = '../vimage/vimage/resource/material/lexi_logo.png'
        default_logo_data = format_image_data(post_data=None, url=None, path=logo_image,
                                              image_type=ImageType.Logo,
                                              width=71, height=79, radius=0, x=50, y=50, z_index=0)

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
            a_image_data = format_image_data(post_data=self.data, url=self.goods_images[0], path=None,
                                             image_type=ImageType.Goods,
                                             width=a_img_w, height=a_img_h, radius=0, x=0, y=0, z_index=0)

            images_style_data.append(a_image_data)

        elif img_count >= 3:
            # 多张图片 只展示3张
            for index in range(len(self.goods_images[:3])):
                img_url = self.goods_images[index]  # 图片地址

                image_x = 0 if index == 0 else f_img_w + 2  # 图片的x间隔
                image_y = 0 if index < 2 else m_img_w + 3  # 图片的y间隔
                image_w = f_img_w if index == 0 else m_img_w  # 图片的宽度

                goods_image_data = format_image_data(post_data=self.data, url=img_url, path=None,
                                                     image_type=ImageType.Goods,
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
        logo_image = '../vimage/vimage/resource/material/lexi_logo.png'
        default_logo_data = format_image_data(post_data=None, url=None, path=logo_image, image_type=ImageType.Logo,
                                              width=71,
                                              height=79, radius=0, x=60, y=664 - default_origin_y, z_index=1)

        # 默认名称
        default_name_data = format_text_data(post_data=self.data, text='乐喜', text_type=TextType.Info,
                                             font_size=36, font_family='PingFang Bold', align='left',
                                             text_color='#666666', x=150, y=669 - default_origin_y, spacing=None,
                                             z_index=0)

        # 默认标语
        default_slogan_data = format_text_data(post_data=self.data, text='全球原创设计品位购物平台', text_type=TextType.Info,
                                               font_size=20, font_family='PingFang Bold', align='left',
                                               text_color='#666666', x=150, y=720 - default_origin_y, spacing=None,
                                               z_index=1)

        # 用户头像
        user_avatar_image_data = format_image_data(post_data=self.data, url=None, path=None,
                                                   image_type=ImageType.Avatar,
                                                   width=70, height=70, radius=8, x=60, y=45, z_index=2)

        # 用户昵称
        default_nickname = {'nickname': ('%s  向你推荐了' % self.data.get('nickname'))}
        user_nickname_data = format_text_data(post_data=default_nickname, text=None, text_type=TextType.Nickname,
                                              font_size=28, font_family='PingFang Bold', align='left',
                                              text_color='#FFFFFF', x=150, y=60, spacing=None, z_index=2)

        # 小程序码
        wxa_code_image_data = format_image_data(post_data=self.data, url=None, path=None, image_type=ImageType.WxaCode,
                                                width=180,
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
        coupon_image = '../vimage/vimage/resource/material/ticket_background.png'
        coupon_image_data = format_image_data(post_data=None, url=None, path=coupon_image, image_type=ImageType.Modify,
                                              width=150, height=80, radius=0, x=64, y=408 - not_describe_origin_y,
                                              z_index=4)

        # 背景
        image_url_id = 2 if self.footer_h == 834 else 3
        background_image = ('../vimage/vimage/resource/background/background_%d.png' % image_url_id)
        background_image_data = format_image_data(post_data=None, url=None, path=background_image,
                                                  image_type=ImageType.Background,
                                                  width=self.width, height=self.footer_h - 10, radius=0, x=0, y=10,
                                                  z_index=0)

        images_data = [default_logo_data, user_avatar_image_data, wxa_code_image_data, background_image_data]

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
            a_image_data = format_image_data(post_data=self.data, url=self.goods_images[0], path=None,
                                             image_type=ImageType.Goods,
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

                goods_image_data = format_image_data(post_data=self.data, url=img_url, path=None,
                                                     image_type=ImageType.Goods,
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
        default_title_image = '../vimage/vimage/resource/material/material_1.png'
        default_title_data = format_image_data(post_data=None, url=None, path=default_title_image,
                                               image_type=ImageType.Modify,
                                               width=375, height=61, radius=0, x=50, y=50, z_index=0)

        # 用户头像
        user_avatar_image_data = format_image_data(post_data=self.data, url=None, path=None,
                                                   image_type=ImageType.Avatar,
                                                   width=70, height=70, radius=8, x=50, y=160, z_index=1)

        # 用户昵称
        default_nickname = {'nickname': ('%s  向你推荐了' % self.data.get('nickname'))}
        user_nickname_data = format_text_data(post_data=default_nickname, text=None, text_type=TextType.Nickname,
                                              font_size=28, font_family='PingFang Bold', align='left',
                                              text_color='#333333', x=140, y=175, spacing=None, z_index=0)

        image_count = len(self.goods_images)

        return {
            'size': size,
            'texts': [] if image_count < 3 else [user_nickname_data],
            'images': [] if image_count < 3 else [default_title_data, user_avatar_image_data],
            'shapes': []
        }

    def footer_view(self):
        """
            底部内容视图数据
        """

        size = (self.width, self.footer_h)

        default_origin_y = 0 if self.footer_h == 570 else 144

        # 默认logo
        logo_image = '../vimage/vimage/resource/material/lexi_logo.png'
        default_logo_data = format_image_data(post_data=None, url=None, path=logo_image, image_type=ImageType.Logo,
                                              width=71,
                                              height=79, radius=0, x=50, y=434 + default_origin_y, z_index=1)

        # 默认名称
        default_name_data = format_text_data(post_data=self.data, text='乐喜', text_type=TextType.Info,
                                             font_size=36, font_family='PingFang Bold', align='left',
                                             text_color='#666666', x=140, y=439 + default_origin_y, spacing=None,
                                             z_index=0)

        # 默认标语
        default_slogan_data = format_text_data(post_data=self.data, text='全球原创设计品位购物平台', text_type=TextType.Info,
                                               font_size=20, font_family='PingFang Bold', align='left',
                                               text_color='#666666', x=140, y=490 + default_origin_y, spacing=None,
                                               z_index=1)

        # 用户头像
        user_avatar_image_data = format_image_data(post_data=self.data, url=None, path=None,
                                                   image_type=ImageType.Avatar,
                                                   width=70, height=70, radius=8, x=70, y=45, z_index=2)

        # 用户昵称
        default_nickname = {'nickname': ('%s  向你推荐了' % self.data.get('nickname'))}
        user_nickname_data = format_text_data(post_data=default_nickname, text=None, text_type=TextType.Nickname,
                                              font_size=28, font_family='PingFang Bold', align='left',
                                              text_color='#333333', x=160, y=60, spacing=None, z_index=2)

        # 小程序码
        wxa_code_image_data = format_image_data(post_data=self.data, url=None, path=None, image_type=ImageType.WxaCode,
                                                width=180,
                                                height=180, radius=0, x=514, y=289 + default_origin_y, z_index=3)

        # 提示文字
        hint_text_data = format_text_data(post_data=self.data, text='长按识别小程序码', text_type=TextType.Hint,
                                          font_size=24, font_family=None, align='left', text_color='#666666',
                                          x=508, y=489 + default_origin_y, spacing=None, z_index=3)

        # 商品名称
        title_data = {'title': self.data.get('title')[:20]}
        goods_title_data = format_text_data(post_data=title_data, text=None, text_type=TextType.Title,
                                            font_size=32, font_family='PingFang Bold', align='left',
                                            text_color='#333333', x=50, y=37 + default_origin_y, spacing=None,
                                            z_index=4)

        # 商品推荐语
        describe_content = self.data.get('describe')[:50]
        describe_data = {'describe': describe_content}
        goods_describe_data = format_text_data(post_data=describe_data, text=None, text_type=TextType.Describe,
                                               font_size=26, font_family=None, align='left', text_color='#333333',
                                               x=50, y=90 + default_origin_y, spacing=38, z_index=5, width=650)

        price_origin_y = 0 if len(describe_content) > 24 else 38
        not_describe_origin_y = 96 if len(self.data.get('describe')) == 0 else price_origin_y  # 没有商品推荐语时的顶部边距

        # 商品价格
        default_price = '￥%s' % str(self.data.get('sale_price'))
        goods_price_data = format_text_data(post_data=None, text=default_price, text_type=TextType.SalePrice,
                                            font_size=28, font_family='PingFang Bold', align='left',
                                            text_color='#333333', x=50,
                                            y=183 + default_origin_y - not_describe_origin_y,
                                            spacing=None, z_index=6)

        # 商品原价
        default_price_width = len(default_price) * 28
        original_price = '￥%s' % str(self.data.get('original_price'))
        original_price_data = format_text_data(post_data=None, text=original_price, text_type=TextType.SalePrice,
                                               font_size=24, font_family=None, align='left',
                                               text_color='#999999', x=10 + default_price_width,
                                               y=187 + default_origin_y - not_describe_origin_y,
                                               spacing=None, z_index=7)

        # 优惠红包提示
        coupon_hint_data = format_text_data(post_data=default_price, text='最高优惠红包可领', text_type=TextType.Info,
                                            font_size=24, font_family='PingFang Bold', align='left',
                                            text_color='#999999', x=50,
                                            y=231 + default_origin_y - not_describe_origin_y,
                                            spacing=None, z_index=8)

        # 优惠红包金额
        coupon_amount = ('￥%s' % self.data.get('coupon_amount'))
        coupon_amount_data = format_text_data(post_data=self.data, text=coupon_amount, text_type=TextType.Info,
                                              font_size=32, font_family='PingFang Bold', align='left',
                                              text_color='#FFFFFF', x=90,
                                              y=282 + default_origin_y - not_describe_origin_y,
                                              spacing=None, z_index=9)

        # 优惠红包天数
        coupon_days = ('%s天有效期' % self.data.get('coupon_days'))
        coupon_days_data = format_text_data(post_data=default_price, text=coupon_days, text_type=TextType.Info,
                                            font_size=20, font_family='PingFang Bold', align='left',
                                            text_color='#FFFFFF', x=78,
                                            y=322 + default_origin_y - not_describe_origin_y,
                                            spacing=None, z_index=10)

        # 优惠红包背景
        coupon_image = '../vimage/vimage/resource/material/ticket_background.png'
        coupon_image_data = format_image_data(post_data=None, url=None, path=coupon_image, image_type=ImageType.Modify,
                                              width=150, height=80, radius=0, x=50,
                                              y=275 + default_origin_y - not_describe_origin_y,
                                              z_index=4)

        # 背景
        background_image = '../vimage/vimage/resource/background/background_4.png'
        background_image_data = format_image_data(post_data=None, url=None, path=background_image,
                                                  image_type=ImageType.Background,
                                                  width=self.width, height=self.footer_h, radius=0, x=0, y=0, z_index=0)

        images_data = [default_logo_data, wxa_code_image_data]

        texts_data = [default_name_data, default_slogan_data, hint_text_data, goods_title_data,
                      goods_describe_data, goods_price_data]

        shapes_data = []

        # 原价的删除线
        original_origin_w = len(original_price) * 15
        original_origin_x = 10 + default_price_width
        original_origin_y = 203 + default_origin_y - not_describe_origin_y
        draw_line_data = format_shape_data(shape_type=DrawShapeType.Line,
                                           position=[(original_origin_x, original_origin_y),
                                                     (original_origin_x + original_origin_w, original_origin_y)],
                                           width=1, color='#999999', out_color=None, z_index=0)

        if self.footer_h == 714:
            images_data.append(user_avatar_image_data)
            images_data.append(background_image_data)
            texts_data.append(user_nickname_data)

        if self.data.get('coupon_amount') is not None and int(self.data.get('coupon_amount')) > 0:
            images_data.append(coupon_image_data)
            texts_data.append(coupon_hint_data)
            texts_data.append(coupon_amount_data)
            texts_data.append(coupon_days_data)

        if self.data.get('original_price') is not None and int(self.data.get('original_price')) > 0:
            texts_data.append(original_price_data)
            shapes_data.append(draw_line_data)

        return {
            'size': size,
            'texts': texts_data,
            'images': images_data,
            'shapes': shapes_data
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


class InviteFriendsPosterStyle:
    """
        邀请好友分享海报样式
    """

    def __init__(self, post_data):
        """
        初始化样式

        :param post_data: 海报数据
        """

        self.data = post_data or {}

        self.color = (255, 255, 255)
        self.width = Size.POSTER_IMAGE_SIZE['width']
        self.height = Size.POSTER_IMAGE_SIZE['height']
        self.size = (self.width, self.height)

    @property
    def info_view(self):
        """
            信息视图
        """

        # 用户头像
        user_avatar_image_data = format_image_data(post_data=self.data, url=None, path=None,
                                                   image_type=ImageType.Avatar,
                                                   width=192, height=192, radius=96, x=279, y=183, z_index=5)

        # 用户昵称
        user_nickname_data = format_text_data(post_data=self.data, text=None, text_type=TextType.Nickname,
                                              font_size=36, font_family='PingFang Bold', align='center',
                                              text_color='#333333', x=100, y=407, spacing=None, z_index=1)

        # 默认邀请提示语
        default_invite_data = format_text_data(post_data=None, text='邀请你一起来乐喜', text_type=TextType.Info,
                                               font_size=28, font_family=None, align='center',
                                               text_color='#999999', x=100, y=473, spacing=None, z_index=2)

        # 默认邀请标语
        invite_title_data = format_text_data(post_data=None, text='开一个能赚钱的生活馆', text_type=TextType.Info,
                                             font_size=48, font_family='PingFang Bold', align='center',
                                             text_color='#333333', x=120, y=525, spacing=None, z_index=3)

        # 默认邀请内容
        invite_content_data = format_text_data(post_data=None, text='零成本开馆，动动手指轻松赚取收入', text_type=TextType.Info,
                                               font_size=26, font_family=None, align='center',
                                               text_color='#D5AF83', x=120, y=599, spacing=None, z_index=5)

        # 默认邀请 slogan
        invite_slogan_data = format_text_data(post_data=None, text='品位设计，美感生活', text_type=TextType.Info,
                                              font_size=26, font_family=None, align='center',
                                              text_color='#D5AF83', x=120, y=645, spacing=None, z_index=6)

        # 开馆人数
        people_count = ('当前已有%s人开馆' % str(self.data.get('people_count')))
        open_number_data = format_text_data(post_data=None, text=people_count, text_type=TextType.Info,
                                            font_size=22, font_family='PingFang Bold', align='center',
                                            text_color='#FFFFFF', x=260, y=706, spacing=None, z_index=7)

        # 小程序码
        wxa_code_image_data = format_image_data(post_data=self.data, url=None, path=None, image_type=ImageType.WxaCode,
                                                width=200,
                                                height=200, radius=0, x=277, y=814, z_index=6)

        # 提示文字
        hint_text_data = format_text_data(post_data=self.data, text='长按识别小程序码立即开通', text_type=TextType.Hint,
                                          font_size=24, font_family='PingFang Bold', align='center',
                                          text_color='#333333',
                                          x=230, y=1034, spacing=None, z_index=8)

        # 背景
        background_image = '../vimage/vimage/resource/background/invite_poster_background_0.png'
        background_image_data = format_image_data(post_data=None, url=None, path=background_image,
                                                  image_type=ImageType.Background,
                                                  width=self.width, height=self.height, radius=0, x=0, y=0, z_index=0)

        # 背景 1
        background_image_1 = '../vimage/vimage/resource/background/background_5.png'
        background_image_data_1 = format_image_data(post_data=None, url=None, path=background_image_1,
                                                    image_type=ImageType.Background,
                                                    width=710, height=916, radius=0, x=20, y=258, z_index=1)

        # 素材 1
        modify_image_1 = '../vimage/vimage/resource/material/material_8.png'
        modify_image_data_1 = format_image_data(post_data=None, url=None, path=modify_image_1,
                                                image_type=ImageType.Modify,
                                                width=365, height=47, radius=0, x=181, y=309, z_index=2)

        # 素材 2
        modify_image_2 = '../vimage/vimage/resource/material/material_9.png'
        modify_image_data_2 = format_image_data(post_data=None, url=None, path=modify_image_2,
                                                image_type=ImageType.Modify,
                                                width=585, height=2, radius=0, x=83, y=775, z_index=3)

        # 素材 3
        modify_image_3 = '../vimage/vimage/resource/material/material_7.png'
        modify_image_data_3 = format_image_data(post_data=None, url=None, path=modify_image_3,
                                                image_type=ImageType.Modify,
                                                width=268, height=36, radius=0, x=240, y=704, z_index=4)

        # 头像描边素材
        modify_image_4 = '../vimage/vimage/resource/material/material_26.png'
        modify_image_data_4 = format_image_data(post_data=None, url=None, path=modify_image_4,
                                                image_type=ImageType.Modify,
                                                width=200, height=200, radius=0, x=275, y=179, z_index=6)

        # 默认logo
        logo_image = '../vimage/vimage/resource/material/lexi_logo.png'
        default_logo_data = format_image_data(post_data=None, url=None, path=logo_image, image_type=ImageType.Logo,
                                              width=71,
                                              height=79, radius=0, x=619, y=1177, z_index=3)

        # 默认名称
        default_name_data = format_text_data(post_data=self.data, text='乐喜', text_type=TextType.Info,
                                             font_size=36, font_family='PingFang Bold', align='right',
                                             text_color='#FFFFFF', x=535, y=1182, spacing=None, z_index=9)

        # 默认标语
        default_slogan_data = format_text_data(post_data=self.data, text='全球原创设计品位购物平台', text_type=TextType.Info,
                                               font_size=24, font_family='PingFang Bold', align='right',
                                               text_color='#FFFFFF', x=319, y=1228, spacing=None,
                                               z_index=10)

        images_data = [background_image_data, background_image_data_1, modify_image_data_1, modify_image_data_2,
                       modify_image_data_3, modify_image_data_4, user_avatar_image_data, wxa_code_image_data,
                       default_logo_data]

        texts_data = [user_nickname_data, default_invite_data, invite_title_data, invite_content_data,
                      invite_slogan_data,
                      open_number_data, hint_text_data, default_name_data, default_slogan_data]

        return {
            'size': self.size,
            'texts': texts_data,
            'images': images_data,
            'shapes': []
        }

    def get_style_one(self):
        """
           样式一
        """

        # 视图数据
        info_view = self.info_view

        # 视图集合
        views = [info_view]

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


class InviteFriendsCardStyle:
    """
        邀请好友分享卡片样式
    """

    def __init__(self, post_data):
        """
        初始化样式

        :param post_data: 海报数据
        """

        self.data = post_data or {}

        self.color = (255, 255, 255)
        self.width = 420
        self.height = 336
        self.size = (self.width, self.height)

    @property
    def info_view(self):
        """
            信息视图
        """

        # 用户头像
        user_avatar_image_data = format_image_data(post_data=self.data, url=None, path=None,
                                                   image_type=ImageType.Avatar,
                                                   width=80, height=80, radius=40, x=173, y=17, z_index=6)

        # 头像描边素材
        modify_image_5 = '../vimage/vimage/resource/material/material_26.png'
        modify_image_data_5 = format_image_data(post_data=None, url=None, path=modify_image_5,
                                                image_type=ImageType.Modify,
                                                width=84, height=84, radius=0, x=172, y=15, z_index=7)

        # 默认邀请提示语
        default_invite_data = format_text_data(post_data=None, text='来乐喜开一个', text_type=TextType.Info,
                                               font_size=24, font_family=None, align='center',
                                               text_color='#333333', x=50, y=109, spacing=None, z_index=0)

        # 默认邀请标语
        invite_title_data = format_text_data(post_data=None, text='能赚钱的生活馆', text_type=TextType.Info,
                                             font_size=44, font_family='PingFang Bold', align='center',
                                             text_color='#333333', x=50, y=140, spacing=None, z_index=3)

        # 默认邀请内容
        invite_content_data = format_text_data(post_data=None, text='零成本，轻松赚取收入', text_type=TextType.Info,
                                               font_size=22, font_family=None, align='center',
                                               text_color='#D5AF83', x=100, y=200, spacing=None, z_index=5)

        # 确认文字
        sure_info_data = format_text_data(post_data=None, text='立即开馆', text_type=TextType.Info,
                                          font_size=28, font_family='PingFang Bold', align='left',
                                          text_color='#FFFFFF', x=140, y=245, spacing=None, z_index=6)

        # 背景
        background_image = '../vimage/vimage/resource/background/invite_card_background_0.png'
        background_image_data = format_image_data(post_data=None, url=None, path=background_image,
                                                  image_type=ImageType.Background,
                                                  width=self.width, height=self.height, radius=0, x=0, y=0, z_index=0)

        # 背景 1
        background_image_1 = '../vimage/vimage/resource/background/background_6.png'
        background_image_data_1 = format_image_data(post_data=None, url=None, path=background_image_1,
                                                    image_type=ImageType.Background,
                                                    width=380, height=209, radius=0, x=20, y=57, z_index=1)

        # 素材 1
        modify_image_1 = '../vimage/vimage/resource/material/material_5.png'
        modify_image_data_1 = format_image_data(post_data=None, url=None, path=modify_image_1,
                                                image_type=ImageType.Modify,
                                                width=188, height=60, radius=0, x=113, y=236, z_index=2)

        # 素材 2
        modify_image_2 = '../vimage/vimage/resource/material/material_4.png'
        modify_image_data_2 = format_image_data(post_data=None, url=None, path=modify_image_2,
                                                image_type=ImageType.Modify,
                                                width=24, height=24, radius=0, x=262, y=254, z_index=3)

        # 素材 3
        modify_image_3 = '../vimage/vimage/resource/material/material_12.png'
        modify_image_data_3 = format_image_data(post_data=None, url=None, path=modify_image_3,
                                                image_type=ImageType.Modify,
                                                width=27, height=4, radius=0, x=65, y=213, z_index=4)

        # 素材 4
        modify_image_4 = '../vimage/vimage/resource/material/material_13.png'
        modify_image_data_4 = format_image_data(post_data=None, url=None, path=modify_image_4,
                                                image_type=ImageType.Modify,
                                                width=27, height=4, radius=0, x=325, y=213, z_index=5)

        images_data = [background_image_data, background_image_data_1, modify_image_data_1, modify_image_data_2,
                       modify_image_data_3, modify_image_data_4, user_avatar_image_data, modify_image_data_5]

        texts_data = [default_invite_data, invite_title_data, invite_content_data, sure_info_data]

        return {
            'size': self.size,
            'texts': texts_data,
            'images': images_data,
            'shapes': []
        }

    def get_style_one(self):
        """
           样式一
        """

        # 视图数据
        info_view = self.info_view

        # 视图集合
        views = [info_view]

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


class BrandCardStyle:
    """
        品牌馆分享卡片样式
    """

    def __init__(self, post_data):
        """
        初始化样式

        :param post_data: 海报数据
        """

        self.data = post_data or {}

        self.color = (255, 255, 255)
        self.width = 420
        self.height = 336
        self.size = (self.width, self.height)

    @property
    def info_view(self):
        """
            信息视图
        """

        # 昵称
        nickname = ('%s...' % self.data.get('nickname')[:9]) if len(
            set(self.data.get('nickname'))) > 9 else self.data.get('nickname')
        nickname_data = {'nickname': nickname}
        name_data = format_text_data(post_data=nickname_data, text=None, text_type=TextType.Nickname,
                                     font_size=28, font_family='PingFang Bold', align='center',
                                     text_color='#333333', x=50, y=154, spacing=None, z_index=0)

        # 城市
        city_data = format_text_data(post_data=self.data, text=None, text_type=TextType.City,
                                     font_size=22, font_family=None, align='center',
                                     text_color='#666666', x=100, y=192, spacing=None, z_index=1)

        # 确认文字
        sure_info_data = format_text_data(post_data=None, text='去逛逛', text_type=TextType.Info,
                                          font_size=28, font_family='PingFang Bold', align='left',
                                          text_color='#FFFFFF', x=155, y=273, spacing=None, z_index=2)

        # 背景
        background_image_data = format_image_data(post_data=self.data, url=None, path=None,
                                                  image_type=ImageType.Background,
                                                  width=self.width, height=160, radius=0, x=0, y=0, z_index=0)

        # 背景 1
        background_image_1 = '../vimage/vimage/resource/background/background_9.png'
        background_image_data_1 = format_image_data(post_data=None, url=None, path=background_image_1,
                                                    image_type=ImageType.Background,
                                                    width=400, height=248, radius=0, x=10, y=88, z_index=1)

        # 素材
        modify_image = '../vimage/vimage/resource/material/material_4.png'
        modify_image_data = format_image_data(post_data=None, url=None, path=modify_image, image_type=ImageType.Modify,
                                              width=24, height=24, radius=0, x=256, y=280, z_index=2)

        # 用户头像
        user_avatar_image_data = format_image_data(post_data=self.data, url=None, path=None,
                                                   image_type=ImageType.Avatar,
                                                   width=82, height=82, radius=0, x=167, y=46, z_index=3)

        # 头像描边
        modify_image_1 = '../vimage/vimage/resource/material/material_27.png'
        modify_image_data_1 = format_image_data(post_data=None, url=None, path=modify_image_1,
                                                image_type=ImageType.Modify,
                                                width=86, height=86, radius=0, x=165, y=44, z_index=4)

        images_data = [background_image_data, background_image_data_1, modify_image_data, modify_image_data_1,
                       user_avatar_image_data]

        texts_data = [name_data, city_data, sure_info_data]

        return {
            'size': self.size,
            'texts': texts_data,
            'images': images_data,
            'shapes': []
        }

    def get_style_one(self):
        """
           样式一
        """

        # 视图数据
        info_view = self.info_view

        # 视图集合
        views = [info_view]

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


class LifeCardStyle:
    """
        邀请好友分享卡片样式
    """

    def __init__(self, post_data):
        """
        初始化样式

        :param post_data: 海报数据
        """

        self.data = post_data or {}

        self.color = (255, 255, 255)
        self.width = 420
        self.height = 336
        self.size = (self.width, self.height)

    @property
    def info_view(self):
        """
            信息视图
        """

        # 用户头像
        user_avatar_image_data = format_image_data(post_data=self.data, url=None, path=None,
                                                   image_type=ImageType.Avatar,
                                                   width=86, height=86, radius=4, x=165, y=44, z_index=5)

        # 用户昵称
        nickname = {'nickname': ('%s的生活馆' % self.data.get('nickname')[:8])}
        user_nickname_data = format_text_data(post_data=nickname, text=None, text_type=TextType.Nickname,
                                              font_size=26, font_family='PingFang Bold', align='center',
                                              text_color='#333333', x=50, y=154, spacing=None, z_index=0)

        # 默认邀请提示语
        default_invite_data = format_text_data(post_data=None, text='我在乐喜开了一家原创手作精品店', text_type=TextType.Info,
                                               font_size=22, font_family=None, align='center',
                                               text_color='#666666', x=40, y=195, spacing=None, z_index=1)

        # 确认文字
        sure_info_data = format_text_data(post_data=None, text='去逛逛', text_type=TextType.Info,
                                          font_size=28, font_family='PingFang Bold', align='left',
                                          text_color='#FFFFFF', x=150, y=257, spacing=None, z_index=2)

        # 背景
        background_image = '../vimage/vimage/resource/background/life_card_background_0.png'
        background_image_data = format_image_data(post_data=None, url=None, path=background_image,
                                                  image_type=ImageType.Background,
                                                  width=self.width, height=self.height, radius=0, x=0, y=0, z_index=0)

        # 背景 1
        background_image_1 = '../vimage/vimage/resource/background/background_7.png'
        background_image_data_1 = format_image_data(post_data=None, url=None, path=background_image_1,
                                                    image_type=ImageType.Background,
                                                    width=380, height=187, radius=0, x=20, y=89, z_index=1)

        # 素材 1
        modify_image_1 = '../vimage/vimage/resource/material/material_5.png'
        modify_image_data_1 = format_image_data(post_data=None, url=None, path=modify_image_1,
                                                image_type=ImageType.Modify,
                                                width=188, height=60, radius=0, x=113, y=246, z_index=2)

        # 素材 2
        modify_image_2 = '../vimage/vimage/resource/material/material_4.png'
        modify_image_data_2 = format_image_data(post_data=None, url=None, path=modify_image_2,
                                                image_type=ImageType.Modify,
                                                width=24, height=24, radius=0, x=250, y=265, z_index=3)

        # 素材3
        modify_image_3 = '../vimage/vimage/resource/material/material_15.png'
        modify_image_data_3 = format_image_data(post_data=None, url=None, path=modify_image_3,
                                                image_type=ImageType.Modify,
                                                width=94, height=94, radius=0, x=161, y=40, z_index=4)

        images_data = [background_image_data, background_image_data_1, modify_image_data_1, modify_image_data_2,
                       modify_image_data_3, user_avatar_image_data]

        texts_data = [user_nickname_data, default_invite_data, sure_info_data]

        return {
            'size': self.size,
            'texts': texts_data,
            'images': images_data,
            'shapes': []
        }

    def get_style_one(self):
        """
           样式一
        """

        # 视图数据
        info_view = self.info_view

        # 视图集合
        views = [info_view]

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


class PlatformCardStyle:
    """
        平台分享卡片样式
    """

    def __init__(self, post_data):
        """
        初始化样式

        :param post_data: 海报数据
        """

        self.data = post_data or {}

        self.color = (255, 255, 255)
        self.width = 420
        self.height = 336
        self.size = (self.width, self.height)

    @property
    def info_view(self):
        """
            信息视图
        """

        # 默认邀请提示语
        default_invite_data = format_text_data(post_data=None, text='品味设计 美感生活', text_type=TextType.Info,
                                               font_size=42, font_family='PingFang Bold', align='center',
                                               text_color='#333333', x=45, y=80, spacing=None, z_index=0)

        # 默认邀请 slogan
        invite_slogan_data = format_text_data(post_data=None, text='全球原创设计品位购物平台', text_type=TextType.Info,
                                              font_size=22, font_family=None, align='center',
                                              text_color='#333333', x=70, y=135, spacing=None, z_index=1)

        # 新人领券金额
        coupon_data = format_text_data(post_data=None, text='新人可领1000元', text_type=TextType.Info,
                                       font_size=24, font_family='PingFang Bold', align='center',
                                       text_color='#FF6666', x=70, y=175, spacing=None, z_index=2)

        # 确认文字
        sure_info_data = format_text_data(post_data=None, text='去逛逛', text_type=TextType.Info,
                                          font_size=28, font_family='PingFang Bold', align='left',
                                          text_color='#FFFFFF', x=145, y=237, spacing=None, z_index=2)

        # 背景
        background_image = '../vimage/vimage/resource/background/lexi_card_background_0.png'
        background_image_data = format_image_data(post_data=None, url=None, path=background_image,
                                                  image_type=ImageType.Background,
                                                  width=self.width, height=self.height, radius=0, x=0, y=0, z_index=0)

        # 背景 1
        background_image_1 = '../vimage/vimage/resource/background/background_8.png'
        background_image_data_1 = format_image_data(post_data=None, url=None, path=background_image_1,
                                                    image_type=ImageType.Background,
                                                    width=380, height=212, radius=0, x=20, y=50, z_index=1)

        # 素材 1
        modify_image_1 = '../vimage/vimage/resource/material/material_5.png'
        modify_image_data_1 = format_image_data(post_data=None, url=None, path=modify_image_1,
                                                image_type=ImageType.Modify,
                                                width=188, height=60, radius=0, x=110, y=227, z_index=2)

        # 素材 2
        modify_image_2 = '../vimage/vimage/resource/material/material_4.png'
        modify_image_data_2 = format_image_data(post_data=None, url=None, path=modify_image_2,
                                                image_type=ImageType.Modify,
                                                width=24, height=24, radius=0, x=245, y=244, z_index=3)

        # 素材3
        modify_image_3 = '../vimage/vimage/resource/material/material_11.png'
        modify_image_data_3 = format_image_data(post_data=None, url=None, path=modify_image_3,
                                                image_type=ImageType.Modify,
                                                width=59, height=70, radius=0, x=20, y=160, z_index=4)

        # 素材4
        modify_image_4 = '../vimage/vimage/resource/material/material_10.png'
        modify_image_data_4 = format_image_data(post_data=None, url=None, path=modify_image_4,
                                                image_type=ImageType.Modify,
                                                width=90, height=73, radius=0, x=279, y=50, z_index=5)

        # 素材5
        modify_image_5 = '../vimage/vimage/resource/material/material_6.png'
        modify_image_data_5 = format_image_data(post_data=None, url=None, path=modify_image_5,
                                                image_type=ImageType.Modify,
                                                width=215, height=35, radius=0, x=100, y=175, z_index=6)

        images_data = [background_image_data, background_image_data_1, modify_image_data_1, modify_image_data_2,
                       modify_image_data_3, modify_image_data_4, modify_image_data_5]

        texts_data = [default_invite_data, invite_slogan_data, coupon_data, sure_info_data]

        return {
            'size': self.size,
            'texts': texts_data,
            'images': images_data,
            'shapes': []
        }

    def get_style_one(self):
        """
           样式一
        """

        # 视图数据
        info_view = self.info_view

        # 视图集合
        views = [info_view]

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


class CouponsCartStyle:
    """
        优惠券分享卡片样式
    """

    def __init__(self, post_data):
        """
        初始化样式

        :param post_data: 海报数据
        """

        self.data = post_data or {}

        self.color = (255, 255, 255)
        self.width = 420
        self.height = 336
        self.size = (self.width, self.height)

    @property
    def info_view(self):
        """
            信息视图
        """

        # 用户昵称
        user_nickname_data = format_text_data(post_data=self.data, text=None, text_type=TextType.Nickname,
                                              font_size=28, font_family='PingFang Bold', align='center',
                                              text_color='#FFFFFF', x=50, y=88, spacing=None, z_index=0)

        # 默认邀请提示语
        default_invite_data = format_text_data(post_data=None, text='让你来领1个乐喜红包', text_type=TextType.Info,
                                               font_size=24, font_family=None, align='center',
                                               text_color='#FFFFFF', x=50, y=126, spacing=None, z_index=1)

        # 新人领券金额
        coupon_data = format_text_data(post_data=None, text='50-800', text_type=TextType.Info,
                                       font_size=56, font_family='PingFang Bold', align=None,
                                       text_color='#FFFFFF', x=88, y=260, spacing=None, z_index=2)

        coupon_hint_data = format_text_data(post_data=None, text='元', text_type=TextType.Info,
                                            font_size=30, font_family='PingFang Bold', align=None,
                                            text_color='#FFFFFF', x=300, y=284, spacing=None, z_index=3)

        # 背景
        background_image = '../vimage/vimage/resource/background/background_10.jpg'
        background_image_data = format_image_data(post_data=None, url=None, path=background_image,
                                                  image_type=ImageType.Background, width=self.width, height=self.height,
                                                  radius=0, x=0, y=0, z_index=0)

        # 用户头像
        user_avatar_image_data = format_image_data(post_data=self.data, url=None, path=None,
                                                   image_type=ImageType.Avatar,
                                                   width=64, height=64, radius=32, x=180, y=14, z_index=1)

        # 头像描边素材
        modify_image = '../vimage/vimage/resource/material/material_26.png'
        modify_image_data = format_image_data(post_data=None, url=None, path=modify_image,
                                              image_type=ImageType.Modify,
                                              width=70, height=70, radius=0, x=176, y=10, z_index=2)

        images_data = [background_image_data, user_avatar_image_data, modify_image_data]

        texts_data = [user_nickname_data, default_invite_data, coupon_data, coupon_hint_data]

        return {
            'size': self.size,
            'texts': texts_data,
            'images': images_data,
            'shapes': []
        }

    def get_style_one(self):
        """
           样式一
        """

        # 视图数据
        info_view = self.info_view

        # 视图集合
        views = [info_view]

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


class GuessGamePosterStyle:
    """
        '猜图赢现金'分享海报样式
    """

    def __init__(self, post_data):
        """
        初始化样式

        :param post_data: 海报数据
        """

        self.data = post_data or {}

        self.color = (255, 255, 255)
        self.width = Size.POSTER_IMAGE_SIZE['width']
        self.height = Size.POSTER_IMAGE_SIZE['height']
        self.size = (self.width, self.height)
        self.randomIndex = random.randint(0, 3)

    @property
    def text_content_data(self):
        """
            文字内容
        """

        # 用户昵称
        nickname_data = format_text_data(post_data=self.data, text=None, text_type=TextType.Nickname,
                                         font_size=40, font_family='PingFang Bold', align='center',
                                         text_color='#333333', x=100, y=280, spacing=None, z_index=1)

        # 默认邀请提示语
        invite_text_data = format_text_data(post_data=None, text='邀请你一起来玩', text_type=TextType.Info,
                                            font_size=30, font_family=None, align='left',
                                            text_color='#666666', x=195, y=350, spacing=None, z_index=2)

        # 默认邀请标语
        invite_title_data = format_text_data(post_data=None, text='猜图赢现金', text_type=TextType.Info,
                                             font_size=30, font_family='PingFang Bold', align='left',
                                             text_color='#FF4069', x=408, y=350, spacing=None, z_index=3)

        # 奖金池内容
        bonus_hint_data = format_text_data(post_data=None, text='奖金池剩余', text_type=TextType.Info,
                                           font_size=26, font_family='PingFang Bold', align='center',
                                           text_color='#F5EAFF', x=200, y=442, spacing=None, z_index=4)

        # 奖金池金额
        bonus_total_amount_text = '%s元' % str(self.data.get('bonus_total_amount'))
        bonus_money_data = format_text_data(post_data=None, text=bonus_total_amount_text, text_type=TextType.Info,
                                            font_size=56, font_family='PingFang Bold', align='center',
                                            text_color='#F5EAFF', x=100, y=483, spacing=None, z_index=5)

        # 红包、优惠券金额
        red_envelope_value = str(self.data.get('bonus_amount'))
        coupon_count = str(self.data.get('coupon_count'))
        red_envelope_text = '获得现金红包 %s 元，获得乐喜优惠券 %s 张' % (red_envelope_value, coupon_count)
        red_envelope_data = format_text_data(post_data=None, text=red_envelope_text, text_type=TextType.Info,
                                             font_size=22, font_family=None, align='center',
                                             text_color='#666666', x=100, y=611, spacing=None, z_index=6)

        # 省钱金额提示
        coupon_hint_text = '购物最高可省 %s 元' % str(self.data.get('save_money_amount'))
        coupon_hint_data = format_text_data(post_data=None, text=coupon_hint_text, text_type=TextType.Info,
                                            font_size=22, font_family=None, align='center',
                                            text_color='#666666', x=100, y=645, spacing=None, z_index=7)

        # 猜图提示
        guess_text_data = format_text_data(post_data=None, text='你也来猜猜这是个什么？', text_type=TextType.Info,
                                           font_size=30, font_family='PingFang Bold', align='left',
                                           text_color='#333333', x=113, y=740, spacing=None, z_index=8)

        # 猜图提示文字
        guess_hint_data = format_text_data(post_data=None, text='(猜对拿现金)', text_type=TextType.Info,
                                           font_size=24, font_family='PingFang Bold', align='left',
                                           text_color='#FF6666', x=442, y=744, spacing=None, z_index=9)

        # 猜图答案 1
        answer_text_data_1 = {'0': '手账本',
                              '1': '牛皮单肩包',
                              '2': '头层牛皮手提包',
                              '3': '笔记本'}
        answer_text_1 = answer_text_data_1.get(str(self.randomIndex))
        answer_origin_x_1 = len(answer_text_1) * 15
        answer_data_1 = format_text_data(post_data=None, text=answer_text_1, text_type=TextType.Info,
                                         font_size=30, font_family='PingFang Bold', align='left',
                                         text_color='#773B02', x=480 - answer_origin_x_1, y=829, spacing=None,
                                         z_index=9)

        # 猜图答案 2
        answer_text_data_2 = {'0': '手表',
                              '1': '双肩包',
                              '2': '原创设计衬衣',
                              '3': '手工钢笔'}
        answer_text_2 = answer_text_data_2.get(str(self.randomIndex))
        answer_origin_x_2 = len(answer_text_2) * 15
        answer_data_2 = format_text_data(post_data=None, text=answer_text_2, text_type=TextType.Info,
                                         font_size=30, font_family='PingFang Bold', align='left',
                                         text_color='#773B02', x=480 - answer_origin_x_2, y=929, spacing=None,
                                         z_index=9)

        # 扫码提示文字
        scan_hint_data = format_text_data(post_data=self.data, text='长按扫码立即猜图', text_type=TextType.Hint,
                                          font_size=24, font_family='PingFang Bold', align='left',
                                          text_color='#D1ACFF', x=504, y=1255, spacing=None, z_index=10)

        # 默认名称
        default_name_data = format_text_data(post_data=self.data, text='乐喜', text_type=TextType.Info,
                                             font_size=30, font_family='PingFang Bold', align='left',
                                             text_color='#FFFFFF', x=126, y=44, spacing=None, z_index=11)

        # 默认标语
        default_slogan_data = format_text_data(post_data=self.data, text='全球原创设计品位购物平台', text_type=TextType.Info,
                                               font_size=22, font_family=None, align='left',
                                               text_color='#B7B7B7', x=126, y=87, spacing=None, z_index=12)

        return [nickname_data, invite_text_data, invite_title_data, bonus_hint_data, bonus_money_data,
                red_envelope_data, coupon_hint_data, guess_text_data, guess_hint_data, answer_data_1,
                answer_data_2, scan_hint_data, default_name_data, default_slogan_data]

    @property
    def image_content_data(self):
        """
            图片素材内容
        """

        # 背景
        background_image = '../vimage/vimage/resource/background/background_11.png'
        background_image_data = format_image_data(post_data=None, url=None, path=background_image,
                                                  image_type=ImageType.Background,
                                                  width=self.width, height=self.height, radius=0, x=0, y=0, z_index=0)

        # 背景 1
        background_image_1 = '../vimage/vimage/resource/background/background_12.png'
        background_image_data_1 = format_image_data(post_data=None, url=None, path=background_image_1,
                                                    image_type=ImageType.Background,
                                                    width=650, height=840, radius=0, x=50, y=195, z_index=1)

        # 素材 1
        modify_image_1 = '../vimage/vimage/resource/material/material_19.png'
        modify_image_data_1 = format_image_data(post_data=None, url=None, path=modify_image_1,
                                                image_type=ImageType.Modify,
                                                width=650, height=248, radius=0, x=50, y=400, z_index=2)

        # 素材 2
        modify_image_2 = '../vimage/vimage/resource/material/material_18.png'
        modify_image_data_2 = format_image_data(post_data=None, url=None, path=modify_image_2,
                                                image_type=ImageType.Modify,
                                                width=580, height=6, radius=0, x=83, y=703, z_index=3)

        # 素材 3
        modify_image_3 = '../vimage/vimage/resource/material/material_20.png'
        modify_image_data_3 = format_image_data(post_data=None, url=None, path=modify_image_3,
                                                image_type=ImageType.Modify,
                                                width=294, height=80, radius=0, x=338, y=810, z_index=4)

        # 素材 4
        modify_image_4 = '../vimage/vimage/resource/material/material_20.png'
        modify_image_data_4 = format_image_data(post_data=None, url=None, path=modify_image_4,
                                                image_type=ImageType.Modify,
                                                width=294, height=80, radius=0, x=338, y=910, z_index=5)

        # 素材 5
        modify_image_5 = '../vimage/vimage/resource/material/material_22.png'
        modify_image_data_5 = format_image_data(post_data=None, url=None, path=modify_image_5,
                                                image_type=ImageType.Modify,
                                                width=62, height=62, radius=0, x=404, y=99, z_index=6)

        # 素材 6
        modify_image_6 = '../vimage/vimage/resource/material/material_17.png'
        modify_image_data_6 = format_image_data(post_data=None, url=None, path=modify_image_6,
                                                image_type=ImageType.Modify,
                                                width=140, height=140, radius=0, x=530, y=1082, z_index=7)

        # 默认logo
        logo_image = '../vimage/vimage/resource/material/lexi_logo.png'
        default_logo_data = format_image_data(post_data=None, url=None, path=logo_image, image_type=ImageType.Logo,
                                              width=58, height=64, radius=0, x=48, y=45, z_index=8)
        # 用户头像
        user_avatar_image_data = format_image_data(post_data=self.data, url=None, path=None,
                                                   image_type=ImageType.Avatar,
                                                   width=130, height=130, radius=65, x=310, y=130, z_index=9)

        # 头像描边素材
        modify_image_7 = '../vimage/vimage/resource/material/material_26.png'
        modify_image_data_7 = format_image_data(post_data=None, url=None, path=modify_image_7,
                                                image_type=ImageType.Modify,
                                                width=138, height=138, radius=0, x=306, y=126, z_index=10)

        # 小程序码
        wxa_code_image_data = format_image_data(post_data=self.data, url=None, path=None, image_type=ImageType.WxaCode,
                                                width=200, height=200, radius=100, x=60, y=1082, z_index=11)

        # 题目图片
        guess_image = '../vimage/vimage/resource/material/guess_material_%d.jpg' % self.randomIndex
        guess_image_data = format_image_data(post_data=None, url=None, path=guess_image, image_type=ImageType.Guess,
                                             width=196, height=196, radius=20, x=112, y=802, z_index=12)

        return [background_image_data, background_image_data_1, modify_image_data_1, modify_image_data_2,
                modify_image_data_3, modify_image_data_4, modify_image_data_5, modify_image_data_6, modify_image_data_7,
                user_avatar_image_data, wxa_code_image_data, default_logo_data, guess_image_data]

    def get_style_first(self):
        """
           样式一
        """

        # 视图数据
        info_content_data = {
            'size': self.size,
            'texts': self.text_content_data,
            'images': self.image_content_data,
            'shapes': []
        }

        # 视图集合
        views = [info_content_data]

        return {
            'size': self.size,
            'color': self.color,
            'views': views
        }

    def get_friends_avatar(self):
        """
            获取好友头像
        """

        if not self.data.get('friends'):
            return []

        friends = self.data.get('friends')
        friend_avatar = []

        for idx, val in enumerate(friends[:4]):
            avatar_image_data = format_image_data(post_data=val, url=None, path=None, image_type=ImageType.Avatar,
                                                  width=40, height=40, radius=20, x=80, y=710 + 60 * idx,
                                                  z_index=12 + idx)
            friend_avatar.append(avatar_image_data)

        return friend_avatar

    def get_friends_name(self):
        """
            获取好友昵称
        """

        if not self.data.get('friends'):
            return []

        friends = self.data.get('friends')
        friend_name = []

        for idx, val in enumerate(friends[:4]):
            name = val.get('nickname')
            cut_name = name[1:-1]
            name = name.replace(cut_name, '*' * len(cut_name))

            if len(name) == 2:
                name = name.replace(name[1:], '*')

            name_data = '%s   已获得' % name
            nickname_data = format_text_data(post_data=None, text=name_data, text_type=TextType.Nickname,
                                             font_size=22, font_family=None, align='left',
                                             text_color='#333333', x=140, y=716 + 59 * idx, spacing=None, z_index=17 + idx)
            friend_name.append(nickname_data)

        return friend_name

    def get_friends_bonus(self):
        """
            好友获取的奖金
        """

        if not self.data.get('friends'):
            return []

        friends = self.data.get('friends')
        friend_bonus = []

        for idx, val in enumerate(friends[:4]):
            name = '%s已获得' % val.get('nickname')
            bonus_amount_data = '%s元' % str(val.get('bonus_amount'))
            origin_x = len(name) * 22 + 15
            bonus_data = format_text_data(post_data=None, text=bonus_amount_data, text_type=TextType.Info,
                                          font_size=24, font_family='PingFang Bold', align='left',
                                          text_color='#FF3F69', x=origin_x + 140, y=714 + 59 * idx, spacing=None, z_index=17 + idx)
            friend_bonus.append(bonus_data)

        return friend_bonus

    @property
    def text_content_data_2(self):
        """
            文字内容
        """

        # 用户昵称
        nickname_data = format_text_data(post_data=self.data, text=None, text_type=TextType.Nickname,
                                         font_size=40, font_family='PingFang Bold', align='center',
                                         text_color='#333333', x=100, y=280, spacing=None, z_index=1)

        # 默认邀请提示语
        invite_text_data = format_text_data(post_data=None, text='在乐喜               活动中', text_type=TextType.Info,
                                            font_size=30, font_family=None, align='left',
                                            text_color='#666666', x=220, y=350, spacing=None, z_index=2)

        # 默认邀请标语
        invite_title_data = format_text_data(post_data=None, text='猜图赢现金', text_type=TextType.Info,
                                             font_size=30, font_family='PingFang Bold', align='left',
                                             text_color='#FF4069', x=311, y=349.6, spacing=None, z_index=3)

        # 奖金内容
        bonus_hint_data = format_text_data(post_data=None, text='总计获得现金红包', text_type=TextType.Info,
                                           font_size=24, font_family=None, align='left',
                                           text_color='#333333', x=127, y=436, spacing=None, z_index=4)

        # 奖金金额
        bonus_amount_text = str(self.data.get('bonus_amount'))
        bonus_amount_text_w = int(len(bonus_amount_text) * 33)
        bonus_amount_text_x = 210 - (bonus_amount_text_w / 2)
        bonus_money_data = format_text_data(post_data=None, text=bonus_amount_text, text_type=TextType.Info,
                                            font_size=65, font_family='PingFang Bold', align='left',
                                            text_color='#FF4069', x=bonus_amount_text_x, y=477, spacing=None, z_index=5)

        bonus_yuan_data = format_text_data(post_data=None, text='元', text_type=TextType.Info,
                                           font_size=30, font_family='PingFang Bold', align='left',
                                           text_color='#FF4069', x=330, y=512, spacing=None, z_index=6)

        # 优惠券内容
        coupon_hint_data = format_text_data(post_data=None, text='总计获得乐喜优惠券金额', text_type=TextType.Info,
                                            font_size=24, font_family=None, align='left',
                                            text_color='#333333', x=388, y=435, spacing=None, z_index=7)

        coupon_money_text = str(self.data.get('coupon_amount'))
        coupon_money_text_w = int(len(coupon_money_text) * 33)
        coupon_money_text_x = 500 - (coupon_money_text_w / 2)
        coupon_money_data = format_text_data(post_data=None, text=coupon_money_text, text_type=TextType.Info,
                                             font_size=65, font_family=None, align='left',
                                             text_color='#FF4069', x=coupon_money_text_x, y=477, spacing=None, z_index=8)

        coupon_yuan_data = format_text_data(post_data=None, text='元', text_type=TextType.Info,
                                            font_size=30, font_family='PingFang Bold', align='left',
                                            text_color='#FF4069', x=620, y=512, spacing=None, z_index=9)

        # 正确数量
        right_count_text = '答对 %s 题' % str(self.data.get('right_count'))
        right_count_data = format_text_data(post_data=None, text=right_count_text, text_type=TextType.Info,
                                            font_size=30, font_family=None, align='left',
                                            text_color='#666666', x=200, y=595, spacing=None, z_index=10)

        # 排名
        ranking_text = '好友榜 第%s名' % str(self.data.get('ranking'))
        ranking_data = format_text_data(post_data=None, text=ranking_text, text_type=TextType.Info,
                                        font_size=30, font_family=None, align='left',
                                        text_color='#666666', x=385, y=595, spacing=None, z_index=11)

        # 猜图提示
        guess_text_data = format_text_data(post_data=None, text='其他好友的好运气', text_type=TextType.Info,
                                           font_size=22, font_family='PingFang Bold', align='left',
                                           text_color='#333333', x=288, y=660, spacing=None, z_index=12)

        # 扫码提示文字
        scan_hint_data = format_text_data(post_data=self.data, text='长按扫码立即猜图', text_type=TextType.Hint,
                                          font_size=24, font_family='PingFang Bold', align='left',
                                          text_color='#D1ACFF', x=504, y=1205, spacing=None, z_index=13)

        # 默认名称
        default_name_data = format_text_data(post_data=self.data, text='乐喜', text_type=TextType.Info,
                                             font_size=30, font_family='PingFang Bold', align='left',
                                             text_color='#FFFFFF', x=126, y=44, spacing=None, z_index=14)

        # 默认标语
        default_slogan_data = format_text_data(post_data=self.data, text='全球原创设计品位购物平台', text_type=TextType.Info,
                                               font_size=22, font_family=None, align='left',
                                               text_color='#B7B7B7', x=126, y=87, spacing=None, z_index=15)

        # 默认标语2
        default_slogan_data_2 = format_text_data(post_data=self.data, text='◆ 全球原创设计新零售服务社区 ◆', text_type=TextType.Info,
                                                 font_size=24, font_family=None, align='center',
                                                 text_color='#B7B7B7', x=50, y=1286, spacing=None, z_index=16)

        texts_data = [nickname_data, invite_text_data, invite_title_data, bonus_hint_data, coupon_hint_data, bonus_money_data,
                      bonus_yuan_data, coupon_money_data, coupon_yuan_data, right_count_data, ranking_data, guess_text_data,
                      scan_hint_data, default_name_data, default_slogan_data, default_slogan_data_2]

        texts_data.extend(self.get_friends_name())
        texts_data.extend(self.get_friends_bonus())

        return texts_data

    @property
    def image_content_data_2(self):
        """
            图片素材内容
        """

        # 背景
        background_image = '../vimage/vimage/resource/background/background_11.png'
        background_image_data = format_image_data(post_data=None, url=None, path=background_image,
                                                  image_type=ImageType.Background,
                                                  width=self.width, height=self.height, radius=0, x=0, y=0, z_index=0)

        # 背景 1
        background_image_1 = '../vimage/vimage/resource/background/background_13.png'
        background_image_data_1 = format_image_data(post_data=None, url=None, path=background_image_1,
                                                    image_type=ImageType.Background,
                                                    width=650, height=763, radius=0, x=50, y=195, z_index=1)

        # 素材 1
        modify_image_1 = '../vimage/vimage/resource/material/material_21.png'
        modify_image_data_1 = format_image_data(post_data=None, url=None, path=modify_image_1,
                                                image_type=ImageType.Modify,
                                                width=670, height=232, radius=0, x=40, y=400, z_index=2)

        # 素材 5
        modify_image_5 = '../vimage/vimage/resource/material/material_22.png'
        modify_image_data_5 = format_image_data(post_data=None, url=None, path=modify_image_5,
                                                image_type=ImageType.Modify,
                                                width=62, height=62, radius=0, x=404, y=99, z_index=3)

        # 素材 6
        modify_image_6 = '../vimage/vimage/resource/material/material_17.png'
        modify_image_data_6 = format_image_data(post_data=None, url=None, path=modify_image_6,
                                                image_type=ImageType.Modify,
                                                width=140, height=140, radius=0, x=530, y=1022, z_index=4)

        # 默认logo
        logo_image = '../vimage/vimage/resource/material/lexi_logo.png'
        default_logo_data = format_image_data(post_data=None, url=None, path=logo_image, image_type=ImageType.Logo,
                                              width=58, height=64, radius=0, x=48, y=45, z_index=5)

        # 用户头像
        user_avatar_image_data = format_image_data(post_data=self.data, url=None, path=None, image_type=ImageType.Avatar,
                                                   width=130, height=130, radius=65, x=310, y=130, z_index=6)

        # 头像描边素材
        modify_image_7 = '../vimage/vimage/resource/material/material_26.png'
        modify_image_data_7 = format_image_data(post_data=None, url=None, path=modify_image_7,
                                                image_type=ImageType.Modify,
                                                width=138, height=138, radius=0, x=306, y=126, z_index=7)

        # 小程序码
        wxa_code_image_data = format_image_data(post_data=self.data, url=None, path=None, image_type=ImageType.WxaCode,
                                                width=200, height=200, radius=100, x=60, y=1022, z_index=8)

        images_data = [background_image_data, background_image_data_1, modify_image_data_1, modify_image_data_5,
                       modify_image_data_6, modify_image_data_7,
                       user_avatar_image_data, wxa_code_image_data, default_logo_data]

        images_data.extend(self.get_friends_avatar())

        return images_data

    def shape_count_data_2(self):
        """
            图形元素
        """

        # 分割线，图形元素
        draw_line_data = format_shape_data(shape_type=DrawShapeType.Line, position=[(80, 675), (280, 675)],
                                           width=1, color='#EEEEEE', out_color=None, z_index=0)

        draw_line_data_1 = format_shape_data(shape_type=DrawShapeType.Line, position=[(470, 675), (670, 675)],
                                             width=1, color='#EEEEEE', out_color=None, z_index=1)

        draw_line_data_2 = format_shape_data(shape_type=DrawShapeType.Line, position=[(374, 450), (374, 543)],
                                             width=1, color='#FFC0CD', out_color=None, z_index=2)

        return [draw_line_data, draw_line_data_1, draw_line_data_2]

    def get_style_second(self):
        """
            样式二
        """

        # 视图数据
        info_content_data = {
            'size': self.size,
            'texts': self.text_content_data_2,
            'images': self.image_content_data_2,
            'shapes': self.shape_count_data_2()
        }

        # 视图集合
        views = [info_content_data]

        return {
            'size': self.size,
            'color': self.color,
            'views': views
        }

    @property
    def text_content_data_3(self):
        """
            文字内容
        """

        # 用户昵称
        nickname_data = format_text_data(post_data=self.data, text=None, text_type=TextType.Nickname,
                                         font_size=32, font_family='PingFang Bold', align='center',
                                         text_color='#F6E0FF', x=100, y=247, spacing=None, z_index=0)

        # 参与人数
        join_count = str(self.data.get('join_user_count'))
        join_user_data = format_text_data(post_data=None, text=join_count, text_type=TextType.Info,
                                          font_size=40, font_family='PingFang Bold', align='left',
                                          text_color='#FFE700', x=202, y=565, spacing=None, z_index=1)

        # 猜图答案 1
        answer_text_data_1 = {'0': '手账本',
                              '1': '牛皮单肩包',
                              '2': '牛皮手提包',
                              '3': '笔记本'}
        answer_text_1 = answer_text_data_1.get(str(self.randomIndex))
        answer_origin_x_1 = len(answer_text_1) * 15
        answer_data_1 = format_text_data(post_data=None, text=answer_text_1, text_type=TextType.Info,
                                         font_size=32, font_family='PingFang Bold', align='left',
                                         text_color='#7B0B35', x=490 - answer_origin_x_1, y=808, spacing=None,
                                         z_index=2)

        # 猜图答案 2
        answer_text_data_2 = {'0': '手表',
                              '1': '双肩包',
                              '2': '原创衬衣',
                              '3': '手工钢笔'}
        answer_text_2 = answer_text_data_2.get(str(self.randomIndex))
        answer_origin_x_2 = len(answer_text_2) * 15
        answer_data_2 = format_text_data(post_data=None, text=answer_text_2, text_type=TextType.Info,
                                         font_size=32, font_family='PingFang Bold', align='left',
                                         text_color='#7B0B35', x=490 - answer_origin_x_2, y=915, spacing=None,
                                         z_index=3)

        texts_data = [nickname_data, join_user_data, answer_data_1, answer_data_2]

        return texts_data

    @property
    def image_content_data_3(self):
        """
            图片素材内容
        """

        # 背景
        background_image = '../vimage/vimage/resource/background/guess_game_background_2.png'
        background_image_data = format_image_data(post_data=None, url=None, path=background_image,
                                                  image_type=ImageType.Background,
                                                  width=self.width, height=self.height, radius=0, x=0, y=0, z_index=0)

        # 用户头像
        user_avatar_image_data = format_image_data(post_data=self.data, url=None, path=None,
                                                   image_type=ImageType.Avatar,
                                                   width=106, height=106, radius=53, x=324, y=129, z_index=1)

        # 小程序码
        wxa_code_image_data = format_image_data(post_data=self.data, url=None, path=None, image_type=ImageType.WxaCode,
                                                width=156, height=156, radius=78, x=84, y=1140, z_index=2)

        # 题目图片
        guess_image = '../vimage/vimage/resource/material/guess_material_%d.jpg' % self.randomIndex
        guess_image_data = format_image_data(post_data=None, url=None, path=guess_image, image_type=ImageType.Guess,
                                             width=210, height=210, radius=0, x=144, y=787, z_index=3)

        images_data = [background_image_data, user_avatar_image_data, wxa_code_image_data, guess_image_data]

        return images_data

    def get_style_third(self):
        """
            样式三
        """

        # 视图数据
        info_content_data = {
            'size': self.size,
            'texts': self.text_content_data_3,
            'images': self.image_content_data_3,
            'shapes': []
        }

        # 视图集合
        views = [info_content_data]

        return {
            'size': self.size,
            'color': self.color,
            'views': views
        }

    @property
    def text_content_data_4(self):
        """
            文字内容
        """

        # 商品图片数量
        images_count = len(self.data.get('goods_images'))

        # 根据商品数量调整 y 偏移量
        origin_y = 0 if images_count > 0 else 50

        # 设计馆默认名称
        nickname_hint_data = format_text_data(post_data=self.data, text='乐喜原创品牌设计馆', text_type=TextType.Info,
                                              font_size=24, font_family=None, align='left',
                                              text_color='#999999', x=230, y=540 + origin_y, spacing=None, z_index=0)

        # 设计馆名称
        nickname_data = format_text_data(post_data=self.data, text=None, text_type=TextType.BrandName,
                                         font_size=34, font_family='PingFang Bold', align='left',
                                         text_color='#5D5047', x=230, y=577 + origin_y, spacing=None, z_index=1)

        # 设计馆描述
        describe_text = ('%s...' % str(self.data.get('describe'))[:15])
        describe_data = format_text_data(post_data=None, text=describe_text, text_type=TextType.Info,
                                         font_size=24, font_family=None, align='left',
                                         text_color='#472F20', x=230, y=632 + origin_y, spacing=None, z_index=2)

        # 参与人数
        join_count = str(self.data.get('join_user_count'))
        join_user_data = format_text_data(post_data=None, text=join_count, text_type=TextType.Info,
                                          font_size=40, font_family='PingFang Bold', align='left',
                                          text_color='#FFE700', x=203, y=417, spacing=None, z_index=3)

        texts_data = [nickname_hint_data, nickname_data, describe_data, join_user_data]

        return texts_data

    @property
    def image_content_data_4(self):
        """
            图片素材内容
        """

        # 商品图片数量
        images_count = len(self.data.get('goods_images'))

        # 根据商品数量调整 y 偏移量
        origin_y = 0 if images_count > 0 else 50

        # 背景
        background_index = 3 if images_count > 0 else 4
        background_image = '../vimage/vimage/resource/background/guess_game_background_%d.png' % background_index
        background_image_data = format_image_data(post_data=None, url=None, path=background_image,
                                                  image_type=ImageType.Background,
                                                  width=self.width, height=self.height, radius=0, x=0, y=0, z_index=0)

        # 设计馆logo
        brand_logo_data = format_image_data(post_data=self.data, url=None, path=None,
                                            image_type=ImageType.BrandLogo,
                                            width=120, height=120, radius=0, x=90, y=540 + origin_y, z_index=1)

        # 根据商品数量调整 y 偏移量
        wxa_code_origin_y = 0 if images_count > 0 else 90

        # 小程序码
        wxa_code_image_data = format_image_data(post_data=self.data, url=None, path=None, image_type=ImageType.WxaCode,
                                                width=156, height=156, radius=78, x=80, y=1070 - wxa_code_origin_y, z_index=2)

        images_data = [background_image_data, brand_logo_data, wxa_code_image_data]

        # 商品图片
        goods_origin_x = 90
        for images_url in self.data.get('goods_images')[:3]:
            goods_image_data = format_image_data(post_data=None, url=images_url, path=None, image_type=ImageType.Goods,
                                                 width=176, height=176, radius=0, x=goods_origin_x, y=698, z_index=3)
            images_data.append(goods_image_data)
            goods_origin_x += 196

        return images_data

    def get_style_fourth(self):
        """
            样式四
        """

        # 视图数据
        info_content_data = {
            'size': self.size,
            'texts': self.text_content_data_4,
            'images': self.image_content_data_4,
            'shapes': []
        }

        # 视图集合
        views = [info_content_data]

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


class ShopWindowPosterStyle:
    """
        橱窗海报分享样式
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
        self.footer_h = 180
        self.top_h = 280
        self.goods_h = 0
        self.goods_images_style = []    # 图片样式集合

    def images_view_style_1(self):
        """
            三张图的样式
        """

        f_img_w = 498  # 首图宽度
        m_img_w = 248  # 多图宽度

        # 多张图片 只展示3张
        for index in range(len(self.goods_images[:3])):
            img_url = self.goods_images[index]  # 图片地址

            image_x = 0 if index == 0 else f_img_w + 4  # 图片的x间隔
            image_y = 0 if index < 2 else m_img_w + 4  # 图片的y间隔
            image_w = f_img_w if index == 0 else m_img_w  # 图片的宽度
            image_h = f_img_w if index == 0 else m_img_w  # 图片的高度

            goods_image_data = format_image_data(post_data=self.data, url=img_url, path=None,
                                                 image_type=ImageType.Goods,
                                                 width=image_w, height=image_h, radius=0, x=image_x, y=image_y,
                                                 z_index=index + 1)

            self.goods_images_style.append(goods_image_data)

        return self.goods_images_style

    def images_view_style_2(self):
        """
            五张图的样式
        """

        goods_image_w = [460, 286, 286, 430, 315]
        goods_image_h = [460, 228, 228, 322, 322]
        goods_image_x = [0, 464, 464, 0, 434]
        goods_image_y = [0, 0, 232, 464, 464]

        # 多张图片 只展示5张
        for index in range(len(self.goods_images[:5])):
            img_url = self.goods_images[index]  # 图片地址

            goods_image_data = format_image_data(post_data=self.data, url=img_url, path=None,
                                                 image_type=ImageType.Goods,
                                                 width=goods_image_w[index], height=goods_image_h[index], radius=0,
                                                 x=goods_image_x[index], y=goods_image_y[index], z_index=index + 1)

            self.goods_images_style.append(goods_image_data)

        return self.goods_images_style

    def images_view_style_3(self):
        """
            七张图的样式
        """

        goods_image_w = [157, 157, 432, 316, 254, 246, 246]
        goods_image_h = [157, 157, 435, 276, 246, 246, 246]
        goods_image_x = [0, 159, 318, 0, 0, 256, 504]
        goods_image_y = [0, 0, 0, 159, 437, 437, 437]

        # 多张图片 只展示7张
        for index in range(len(self.goods_images[:7])):
            img_url = self.goods_images[index]  # 图片地址

            goods_image_data = format_image_data(post_data=self.data, url=img_url, path=None,
                                                 image_type=ImageType.Goods,
                                                 width=goods_image_w[index], height=goods_image_h[index], radius=0,
                                                 x=goods_image_x[index], y=goods_image_y[index], z_index=index + 1)

            self.goods_images_style.append(goods_image_data)

        return self.goods_images_style

    @property
    def goods_images_view(self):
        """
            图片内容视图
        """

        images_count = len(self.goods_images)

        if images_count == 3:
            self.goods_h = 498
            self.images_view_style_1()

        elif images_count == 5:
            self.goods_h = 787
            self.images_view_style_2()

        elif images_count == 7:
            self.goods_h = 683
            self.images_view_style_3()

        # 标题
        title_text = self.data.get('title')[:34]
        title_data = format_text_data(post_data=None, text=title_text, text_type=TextType.Title,
                                      font_size=40, font_family='PingFang Bold', align='left',
                                      text_color='#25211E', x=30, y=self.goods_h + 30,
                                      spacing=50, z_index=0, width=self.width - 60)

        title_height = (int(get_text_width(title_text, 40) / (self.width - 60)) + 1) * 40 + 10

        # 内容
        describe_content = self.data.get('describe')[:48]
        goods_describe_data = format_text_data(post_data=None, text=describe_content, text_type=TextType.Describe,
                                               font_size=28, font_family=None, align='left', text_color='#666666',
                                               x=30, y=self.goods_h + title_height + 60, spacing=40, z_index=1,
                                               width=self.width - 60)

        # 标签
        tag_text = "#%s" % self.data.get('tag')
        tag_data = format_text_data(post_data=None, text=tag_text, text_type=TextType.Info,
                                    font_size=24, font_family=None, align='left',
                                    text_color='#5FE4B1', x=40, y=self.goods_h + 275, spacing=None, z_index=2)

        # 视图尺寸
        goods_view_h = self.goods_h + 340
        size = (self.width, goods_view_h)

        # 海报的高度
        self.height = self.top_h + self.footer_h + goods_view_h

        return {
            'size': size,
            'texts': [title_data, goods_describe_data, tag_data],
            'images': self.goods_images_style,
            'shapes': []
        }

    def top_view(self):
        """
            顶部内容视图数据
        """

        size = (self.width, self.top_h)

        # 用户昵称
        nickname_data = format_text_data(post_data=self.data, text=None, text_type=TextType.Nickname,
                                         font_size=32, font_family=None, align='left',
                                         text_color='#333333', x=120, y=195, spacing=None, z_index=0)

        # 用户头像
        avatar_url = self.data.get('avatar_img')
        user_avatar_image_data = format_image_data(post_data=None, url=avatar_url, path=None,
                                                   image_type=ImageType.Avatar,
                                                   width=70, height=70, radius=8, x=30, y=180, z_index=0)

        # slogan 素材
        modify_image_1 = '../vimage/vimage/resource/material/material_23.png'
        modify_image_data_1 = format_image_data(post_data=None, url=None, path=modify_image_1,
                                                image_type=ImageType.Modify,
                                                width=720, height=146, radius=0, x=30, y=35, z_index=1)

        return {
            'size': size,
            'texts': [nickname_data],
            'images': [user_avatar_image_data, modify_image_data_1],
            'shapes': []
        }

    def footer_view(self):
        """
            底部内容视图数据
        """

        size = (self.width, self.footer_h)

        # 小程序码
        wxa_code_image_data = format_image_data(post_data=self.data, url=None, path=None,
                                                image_type=ImageType.WxaCode,
                                                width=140, height=140, radius=70, x=30, y=20, z_index=2)

        # 扫码提示
        wxa_hint_data = format_text_data(post_data=None, text='长按识别查看全部内容', text_type=TextType.Info,
                                         font_size=24, font_family=None, align='left',
                                         text_color='#666666', x=190, y=55, spacing=None, z_index=1)

        # 默认标语
        default_slogan_data = format_text_data(post_data=None, text='全球原创设计品位购物平台', text_type=TextType.Info,
                                               font_size=28, font_family='PingFang Bold', align='left',
                                               text_color='#333333', x=190, y=95, spacing=None, z_index=2)

        # 背景
        draw_background_data = format_shape_data(shape_type=DrawShapeType.Rectangle,
                                                 position=[(0, 0), (self.width, self.footer_h)],
                                                 width=1, color='#F7F9FB', out_color=None, z_index=0)

        return {
            'size': size,
            'texts': [wxa_hint_data, default_slogan_data],
            'images': [wxa_code_image_data],
            'shapes': [draw_background_data]
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
            'size': (self.width, self.height),
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


class GoodsCardStyle:
    """
        商品分享卡片样式
    """

    def __init__(self, post_data):
        """
        初始化样式

        :param post_data: 海报数据
        """

        self.data = post_data or {}

        self.color = (255, 255, 255)
        self.width = 420
        self.height = 336
        self.size = (self.width, self.height)

    @property
    def info_view(self):
        """
            信息视图
        """

        # 商品图片
        goods_image_url = self.data.get('goods_images')[0]
        goods_image_data = format_image_data(post_data=None, url=goods_image_url, path=None,
                                             image_type=ImageType.Goods,
                                             width=self.width, height=self.height, radius=0, x=0, y=0, z_index=0)

        # 商品名称
        goods_title = self.data.get('title')
        title_text = '%s...' % goods_title[:13] if len(goods_title) > 13 else goods_title
        goods_title_data = format_text_data(post_data=None, text=title_text, text_type=TextType.Title,
                                            font_size=24, font_family=None, align='left',
                                            text_color='#FFFFFF', x=10, y=278, spacing=None, z_index=0)

        # 素材 1
        modify_image = '../vimage/vimage/resource/material/material_25.png'
        modify_image_data = format_image_data(post_data=None, url=None, path=modify_image,
                                              image_type=ImageType.Modify,
                                              width=360, height=50, radius=0, x=0, y=270, z_index=1)

        images_data = [goods_image_data, modify_image_data]

        texts_data = [goods_title_data]

        return {
            'size': self.size,
            'texts': texts_data,
            'images': images_data,
            'shapes': []
        }

    def get_style_one(self):
        """
           样式一
        """

        # 视图数据
        info_view = self.info_view

        # 视图集合
        views = [info_view]

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