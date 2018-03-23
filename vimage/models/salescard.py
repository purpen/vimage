# -*- coding: utf-8 -*-
from vimage import db
from vimage.helpers.utils import *


class SalesCard(db.Model):
    """
        商品促销卡片
    """

    __tablename__ = 'salescard'

    id = db.Column(db.Integer, primary_key=True)
    # 标题
    sales_title = db.Column(db.String(20), nullable=False)
    # 百分比
    sales_pct = db.Column(db.String(10), nullable=False)
    # 信息
    sales_info = db.Column(db.String(20), nullable=True)
    # 品牌名称
    sales_brand = db.Column(db.String(20), nullable=True)
    # 时间
    time_text = db.Column(db.String(50), nullable=True)
    # 背景图片(url)
    background_img = db.Column(db.Text(), nullable=False)
    # 二维码(url)
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
                    "sales_title": self.sales_title,
                    "sales_pct": self.sales_pct,
                    "sales_info": self.sales_info,
                    "sales_brand": self.sales_brand,
                    "time_text": self.time_text
                },
                "images": {
                    "background_img": self.background_img,
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
