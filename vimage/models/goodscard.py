# -*- coding: utf-8 -*-
from vimage import db
from vimage.helpers.utils import *


class GoodsCard(db.Model):
    """
        商品分享卡片
    """

    __tablename__ = 'goodscard'

    id = db.Column(db.Integer, primary_key=True)
    # 标题
    title = db.Column(db.String(50), nullable=False)
    # 价格
    sale_price = db.Column(db.String(), nullable=False)
    # 品牌名称
    brand_name = db.Column(db.String(10), nullable=True)
    # 默认提示
    hint_text = db.Column(db.String(15), nullable=True)
    # 商品图片(url)
    goods_img = db.Column(db.Text(), nullable=False)
    # 小程序二维码(url)
    qrcode_img = db.Column(db.Text(), nullable=True)
    # logo(url)
    logo_img = db.Column(db.Text(), nullable=True)

    created_at = db.Column(db.Integer, default=timestamp())
    updated_at = db.Column(db.Integer, default=timestamp(), onupdate=timestamp)

    def to_json(self):
        """
            JSON 格式化
        """

        json_post = {
            "data": {
                "texts": {
                    "title": self.title,
                    "sale_price": self.sale_price,
                    "brand_name": self.brand_name,
                    "hint_text": self.hint_text
                },
                "images": {
                    "goods_img": self.goods_img,
                    "qrcode_img": self.qrcode_img,
                    "logo_img": self.logo_img
                }
            },
            # "created_at": self.created_at,
            # "updated_at": self.updated_at,
            "status": custom_status(message='上传成功')
        }

        return json_post

    def __repr__(self):
        return '<GoodsCard {}>'.format(self.id)
