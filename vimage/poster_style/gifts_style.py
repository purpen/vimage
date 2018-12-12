# -*- coding: utf-8 -*-
import math
from vimage.helpers.poster_style_format import *
from vimage.constant import *
from vimage.helpers.switch import *
import random
from vimage.helpers.image_tools import *


class GiftsPosterStyle:
    """
        一元送礼海报
    """

    def __init__(self, post_data):
        """
        初始化海报数据

        :param post_data: 接收数据
        """

        self.data = post_data or {}
        self.type = int(self.data.get('type')) or 1
        self.color = (255, 255, 255)
        self.width = Size.POSTER_IMAGE_SIZE['width']
        self.height = Size.POSTER_IMAGE_SIZE['height']
        self.size = (self.width, self.height)
        self.card_w = 420
        self.card_h = 336

    def get_style_one(self):
        """
           拆礼物样式
        """

        # 用户头像
        user_avatar_image_data = format_image_data(post_data=self.data, url=None, path=None,
                                                   image_type=ImageType.Avatar,
                                                   width=200, height=200, radius=0, x=277, y=180, z_index=1)

        # 商品图片
        goods_image_data = format_image_data(post_data=self.data, url=None, path=None,
                                             image_type=ImageType.Goods,
                                             width=400, height=400, radius=0, x=175, y=512, z_index=2)

        # 小程序码
        wxa_code_image_data = format_image_data(post_data=self.data, url=None, path=None,
                                                image_type=ImageType.WxaCode,
                                                width=212, height=212, radius=0, x=85, y=1030, z_index=3)

        # 背景
        background_image = '../vimage/vimage/resource/background/background_16.png'
        background_image_data = format_image_data(post_data=None, url=None, path=background_image,
                                                  image_type=ImageType.Background,
                                                  width=self.width, height=self.height, radius=0, x=0, y=0, z_index=4)

        # 用户昵称
        nickname = self.data.get('nickname')
        nickname_len = get_text_count(nickname, 28, 160, 'PingFang Bold')
        nickname_text = nickname[:nickname_len]
        user_nickname_data = format_text_data(post_data=None, text=nickname_text, text_type=TextType.Nickname,
                                              font_size=28, font_family='PingFang Bold', align='center',
                                              text_color='#FFFFFF', x=300, y=316, spacing=None, z_index=1)

        # 默认邀请提示语
        default_invite_data = format_text_data(post_data=None, text='送你一个神秘礼物', text_type=TextType.Info,
                                               font_size=56, font_family='PingFang Bold', align='center',
                                               text_color='#856AAF', x=100, y=365, spacing=None, z_index=2)

        # 默认邀请标语
        invite_title_data = format_text_data(post_data=None, text='快来将封印解除', text_type=TextType.Info,
                                             font_size=34, font_family=None, align='center',
                                             text_color='#856AAF', x=253, y=443, spacing=None, z_index=3)

        # 开奖时间
        time_text = '%s开奖' % self.data.get('lottery_time')
        time_data = format_text_data(post_data=None, text=time_text, text_type=TextType.Info,
                                     font_size=24, font_family=None, align='center',
                                     text_color='#FFFFFF', x=170, y=925, spacing=None, z_index=4)

        # 商品原价
        price_text = '原价：¥%s' % str(float(self.data.get('original_price')))
        price_data = format_text_data(post_data=None, text=price_text, text_type=TextType.Info,
                                      font_size=28, font_family='PingFang Bold', align='left',
                                      text_color='#FFFFFF', x=335, y=1150, spacing=None, z_index=5)

        # 原价的删除线
        original_origin_x = 335
        original_origin_y = 1170
        original_origin_w = int(get_text_width(price_text, 28, 'PingFang Bold'))
        draw_line_data = format_shape_data(shape_type=DrawShapeType.Line,
                                           position=[(original_origin_x, original_origin_y),
                                                     (original_origin_x + original_origin_w, original_origin_y)],
                                           width=2, color='#FFFFFF', out_color=None, z_index=0)

        images_data = [user_avatar_image_data, goods_image_data, wxa_code_image_data, background_image_data]

        texts_data = [user_nickname_data, default_invite_data, invite_title_data, time_data, price_data]

        return {
            'size': self.size,
            'texts': texts_data,
            'images': images_data,
            'shapes': [draw_line_data]
        }

    def get_style_two(self):
        """
            炫耀礼物样式
        """

        # 用户头像
        user_avatar_image_data = format_image_data(post_data=self.data, url=None, path=None,
                                                   image_type=ImageType.Avatar,
                                                   width=134, height=134, radius=0, x=308, y=105, z_index=1)

        # 商品图片
        goods_image_data = format_image_data(post_data=self.data, url=None, path=None,
                                             image_type=ImageType.Goods,
                                             width=396, height=396, radius=0, x=179, y=459, z_index=2)

        # 小程序码
        wxa_code_image_data = format_image_data(post_data=self.data, url=None, path=None,
                                                image_type=ImageType.WxaCode,
                                                width=220, height=220, radius=0, x=265, y=951, z_index=3)

        # 背景
        background_image = '../vimage/vimage/resource/background/background_17.png'
        background_image_data = format_image_data(post_data=None, url=None, path=background_image,
                                                  image_type=ImageType.Background,
                                                  width=self.width, height=self.height, radius=0, x=0, y=0, z_index=4)

        # 用户昵称
        nickname = self.data.get('nickname')
        nickname_len = get_text_count(nickname, 28, 160, 'PingFang Bold')
        nickname_text = nickname[:nickname_len]
        user_nickname_data = format_text_data(post_data=None, text=nickname_text, text_type=TextType.Nickname,
                                              font_size=28, font_family='PingFang Bold', align='center',
                                              text_color='#FFFFFF', x=300, y=230, spacing=None, z_index=1)

        # 默认邀请提示语
        default_invite_data = format_text_data(post_data=None, text='OMG！我抽中了', text_type=TextType.Info,
                                               font_size=56, font_family='PingFang Bold', align='center',
                                               text_color='#FA668B', x=100, y=293, spacing=None, z_index=2)

        # 扫码提示语
        hint_text_data = format_text_data(post_data=None, text='扫码我也要拆礼物', text_type=TextType.Info,
                                          font_size=35, font_family='PingFang Bold', align='center',
                                          text_color='#ECF6FF', x=210, y=1201, spacing=None, z_index=3)

        # 商品标题
        goods_title = self.data.get('title')
        goods_title_len = get_text_count(goods_title, 32, 350, None)
        goods_title_text = goods_title[:goods_title_len]
        goods_title_data = format_text_data(post_data=None, text=goods_title_text, text_type=TextType.Title,
                                            font_size=32, font_family=None, align='center',
                                            text_color='#FA668B', x=180, y=377, spacing=None, z_index=4)

        # 商品原价
        price_text = '原价：¥%s' % str(float(self.data.get('original_price')))
        price_data = format_text_data(post_data=None, text=price_text, text_type=TextType.Info,
                                      font_size=28, font_family='PingFang Bold', align='left',
                                      text_color='#FFFFFF', x=180, y=491, spacing=None, z_index=5)

        # 原价的删除线
        original_origin_x = 180
        original_origin_y = 510
        original_origin_w = int(get_text_width(price_text, 28, 'PingFang Bold'))
        draw_line_data = format_shape_data(shape_type=DrawShapeType.Line,
                                           position=[(original_origin_x, original_origin_y),
                                                     (original_origin_x + original_origin_w, original_origin_y)],
                                           width=2, color='#FFFFFF', out_color=None, z_index=0)

        images_data = [user_avatar_image_data, goods_image_data, wxa_code_image_data, background_image_data]

        texts_data = [user_nickname_data, default_invite_data, hint_text_data, goods_title_data, price_data]

        return {
            'size': self.size,
            'texts': texts_data,
            'images': images_data,
            'shapes': [draw_line_data]
        }

    def get_style_three(self):
        """
           邀请拆礼物样式
        """

        # 用户头像
        user_avatar_image_data = format_image_data(post_data=self.data, url=None, path=None,
                                                   image_type=ImageType.Avatar,
                                                   width=126, height=126, radius=0, x=84, y=169, z_index=1)

        # 商品图片
        goods_image_data = format_image_data(post_data=self.data, url=None, path=None,
                                             image_type=ImageType.Goods,
                                             width=400, height=400, radius=0, x=175, y=500, z_index=2)

        # 小程序码
        wxa_code_image_data = format_image_data(post_data=self.data, url=None, path=None,
                                                image_type=ImageType.WxaCode,
                                                width=166, height=166, radius=0, x=74, y=1082, z_index=3)

        # 背景
        background_image = '../vimage/vimage/resource/background/background_20.png'
        background_image_data = format_image_data(post_data=None, url=None, path=background_image,
                                                  image_type=ImageType.Background,
                                                  width=self.width, height=self.height, radius=0, x=0, y=0, z_index=4)

        # 用户昵称
        user_nickname_data = format_text_data(post_data=self.data, text=None, text_type=TextType.Nickname,
                                              font_size=32, font_family='PingFang Bold', align='left',
                                              text_color='#369A7B', x=240, y=184, spacing=None, z_index=1)

        images_data = [user_avatar_image_data, goods_image_data, wxa_code_image_data, background_image_data]

        texts_data = [user_nickname_data]

        return {
            'size': self.size,
            'texts': texts_data,
            'images': images_data,
            'shapes': []
        }

    def get_card_style_one(self):
        """
            拆礼物卡片（带商品）
        """

        # 商品图片
        goods_image_data = format_image_data(post_data=self.data, url=None, path=None,
                                             image_type=ImageType.Goods,
                                             width=240, height=240, radius=0, x=90, y=19, z_index=0)

        # 背景
        background_image = '../vimage/vimage/resource/background/background_19.png'
        background_image_data = format_image_data(post_data=None, url=None, path=background_image,
                                                  image_type=ImageType.Background,
                                                  width=self.card_w, height=self.card_h, radius=0, x=0, y=0, z_index=1)

        # 默认邀请标语
        invite_title_data = format_text_data(post_data=None, text='点击拆礼物', text_type=TextType.Info,
                                             font_size=36, font_family='PingFang Bold', align='center',
                                             text_color='#FEDFE1', x=100, y=247, spacing=None, z_index=0)

        return {
            'size': (self.card_w, self.card_h),
            'texts': [invite_title_data],
            'images': [goods_image_data, background_image_data],
            'shapes': []
        }

    def get_card_style_two(self):
        """
            拆礼物卡片（不带商品）
        """

        # 背景
        background_image = '../vimage/vimage/resource/background/background_18.png'
        background_image_data = format_image_data(post_data=None, url=None, path=background_image,
                                                  image_type=ImageType.Background,
                                                  width=self.card_w, height=self.card_h, radius=0, x=0, y=0, z_index=0)

        # 默认邀请标语
        invite_title_data = format_text_data(post_data=None, text='我也要拆礼物', text_type=TextType.Info,
                                             font_size=36, font_family='PingFang Bold', align='center',
                                             text_color='#FFF7F8', x=100, y=234, spacing=None, z_index=0)

        return {
            'size': (self.card_w, self.card_h),
            'texts': [invite_title_data],
            'images': [background_image_data],
            'shapes': []
        }

    def get_style_data(self):
        """
        获取海报样式数据

        :return: 样式数据
        """

        for case in Switch(self.type):
            if case(1):
                return self.get_style_one()
            if case(2):
                return self.get_style_two()
            if case(3):
                return self.get_card_style_one()
            if case(4):
                return self.get_card_style_two()
            if case(5):
                return self.get_style_three()

        return self.get_style_one()