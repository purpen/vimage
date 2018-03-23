# -*- coding: utf-8 -*-
from vimage import db
from vimage.helpers.utils import timestamp


class ImageSet(db.Model):
    """图片及图形库"""

    __tablename__ = 'imagesets'

    id = db.Column(db.Integer, primary_key=True)
    sn = db.Column(db.String(16), unique=True, nullable=False)
    user_id = db.Column(db.Integer, index=True, default=0)

    filepath = db.Column(db.String(128), unique=True, nullable=False)
    size = db.Column(db.Float, nullable=True)
    width = db.Column(db.Integer, default=0)
    height = db.Column(db.Integer, default=0)
    mime = db.Column(db.String(64), nullable=True)
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

    def to_json(self):

        json = {
            "data": {

            },
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

        return json

    def __repr__(self):
        return '<ImageSet {}>'.format(self.id)
