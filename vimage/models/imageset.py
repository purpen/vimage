# -*- coding: utf-8 -*-
from vimage import db
from vimage.helpers.utils import timestamp

__all__ = [
    'ImageSet',
    'PosterType'
]


class PosterType:
    GOODS_WXA_CODE = 1  # 商品小程序码
    GOODS_PROMOTION_AD = 2  # 商品促销海报


class ImageSet(db.Model):
    """图片及图形库"""

    __tablename__ = 'imagesets'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True, default=0)
    sn = db.Column(db.String(16), unique=True, nullable=False)

    name = db.Column(db.String(64), nullable=True)
    cover_id = db.Column(db.Integer, default=0)
    description = db.Column(db.Text(), nullable=False)
    tags = db.Column(db.String(200))

    # 图片 url
    image = db.Column(db.Text(), nullable=False)

    # 1、样例 2、成品图 3、背景 4、矢量图 5、产品图
    type = db.Column(db.SmallInteger, default=1)
    # 是否审核
    approved = db.Column(db.Boolean, default=False)
    # 1、正常（默认）-1：禁用
    status = db.Column(db.SmallInteger, default=1)

    created_at = db.Column(db.Integer, default=timestamp)
    updated_at = db.Column(db.Integer, default=timestamp, onupdate=timestamp)

    def to_json(self):
        """对象转换"""
        json = {
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

        return json

    def __repr__(self):
        return '<ImageSet {}>'.format(self.sn)
