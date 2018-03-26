# -*- coding: utf-8 -*-
from sqlalchemy import event
from vimage import db
from vimage.helpers.utils import timestamp, MixGenId
from .asset import Asset


__all__ = [
    'Templet'
]


class Templet(db.Model):
    """模板库"""

    __tablename__ = 'templets'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True, default=0)

    sn = db.Column(db.String(16), unique=True, nullable=False)
    name = db.Column(db.String(64), nullable=False)
    cover_id = db.Column(db.Integer, default=0)
    # 模板类型，1、商品小程序码
    type = db.Column(db.SmallInteger, default=1)
    # 使用次数
    use_times = db.Column(db.Integer, default=0)
    # 说明要求
    requirements = db.Column(db.Text(), nullable=True)
    # 1、正常（默认）-1：禁用
    status = db.Column(db.SmallInteger, default=1)

    created_at = db.Column(db.Integer, default=timestamp)
    updated_at = db.Column(db.Integer, default=timestamp, onupdate=timestamp)

    @property
    def type_label(self):
        label = ''
        if self.type == 1:
            label = '小程序商品推广图'

        return label

    @property
    def cover(self):
        """获取封面图"""
        return Asset.query.get(self.cover_id) if self.cover_id else Asset.default_logo()

    @staticmethod
    def make_unique_sn(sn=None):
        """生成模板编号"""
        if sn is None:
            sn = MixGenId.gen_templet_sn()

        if Templet.query.filter_by(sn=sn).first() is None:
            return sn

        while True:
            new_sn = MixGenId.gen_templet_sn()
            if Templet.query.filter_by(sn=new_sn).first() is None:
                break
        return new_sn

    @staticmethod
    def on_before_insert(mapper, connection, target):
        # 自动生成编号
        if target.sn:  # 存在，验证是否唯一
            target.sn = Templet.make_unique_sn(target.serial_no)
        else:
            target.sn = Templet.make_unique_sn()

    def to_json(self):
        """对象转换"""
        json_obj = {
            'sn': self.sn,
            'name': self.name,
            'cover': self.cover.view_url,
            'type': self.type,
            'requirements': self.requirements,
            'status': self.status
        }

        return json_obj

    def __repr__(self):
        return '<Templet {}>'.format(self.sn)


# 监听事件
event.listen(Templet, 'before_insert', Templet.on_before_insert)
