# -*- coding: utf-8 -*-
from vimage import db
from vimage.helpers.utils import timestamp


__all__ = [
    'TextSet'
]


class TextSet(db.Model):
    """文本语料库"""

    __tablename__ = 'textsets'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True, default=0)
    content = db.Column(db.Text(), nullable=False)
    tags = db.Column(db.String(200))
    # 1、单句 2、片段 3、广告语
    type = db.Column(db.SmallInteger, default=1)
    # 是否审核
    approved = db.Column(db.Boolean, default=False)
    # 1、正常（默认）-1：禁用
    status = db.Column(db.SmallInteger, default=1)

    created_at = db.Column(db.Integer, default=timestamp)
    updated_at = db.Column(db.Integer, default=timestamp, onupdate=timestamp)

    def __repr__(self):
        return '<TextSet {}>'.format(self.id)
