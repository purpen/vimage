# -*- coding: utf-8 -*-
from vimage import db
from vimage.helpers.utils import *


class GoodsCard(db.Model):
    """
        商品分享卡片
    """

    __tablename__ = 'goodscard'

    id = db.Column(db.Integer, primary_key=True)
    # 商品图片(url)
    goods_img = db.Column(db.Text(), nullable=False)
    # 标题
    title = db.Column(db.String(50), nullable=False)
    # 价格
    market_price = db.Column(db.Float, nullable=False)
    # 小程序二维码
    wechat_code = db.Column(db.Text(), nullable=True)
    # 小程序名称
    wechat_name = db.Column(db.String(10), nullable=True)
    # 小程序图标
    wechat_icon = db.Column(db.Text(), nullable=True)
    # 默认提示
    default_hint = db.Column(db.String(15), nullable=True, default='长按识别小程序码访问')

    created_at = db.Column(db.Integer, default=timestamp())
    updated_at = db.Column(db.Integer, default=timestamp(), onupdate=timestamp)

    def __repr__(self):
        return '<GoodsCard {}>'.format(self.id)
