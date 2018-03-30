# -*- coding: utf-8 -*-
from sqlalchemy import event
from vimage import db
from vimage.helpers.utils import timestamp, MixGenId
from .asset import Asset

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

    # 1、样例 2、成品图 3、背景 4、矢量图 5、产品图
    type = db.Column(db.SmallInteger, default=1)
    # 是否审核
    approved = db.Column(db.Boolean, default=False)
    # 1、正常（默认）-1：禁用
    status = db.Column(db.SmallInteger, default=1)

    created_at = db.Column(db.Integer, default=timestamp)
    updated_at = db.Column(db.Integer, default=timestamp, onupdate=timestamp)

    @property
    def type_label(self):
        label = ''
        if self.type == 1:
            label = '样例'

        elif self.type == 2:
            label = '成品图'

        elif self.type == 3:
            label = '背景'

        elif self.type == 4:
            label = '矢量图'

        elif self.type == 5:
            label = '产品图'

        return label

    @property
    def cover(self):
        """获取封面图"""
        return Asset.query.get(self.cover_id) if self.cover_id else Asset.default_logo()

    @staticmethod
    def make_unique_sn(sn=None):
        """生成图像编号"""
        if sn is None:
            sn = MixGenId.gen_image_sn()

        if ImageSet.query.filter_by(sn=sn).first() is None:
            return sn

        while True:
            new_sn = MixGenId.gen_image_sn()
            if ImageSet.query.filter_by(sn=new_sn).first() is None:
                break
        return new_sn

    @staticmethod
    def on_before_insert(mapper, connection, target):
        # 自动生成编号
        if target.sn:  # 存在，验证是否唯一
            target.sn = ImageSet.make_unique_sn(target.serial_no)
        else:
            target.sn = ImageSet.make_unique_sn()

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


# 监听事件
event.listen(ImageSet, 'before_insert', ImageSet.on_before_insert)
