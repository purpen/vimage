# -*- coding: utf-8 -*-
from vimage import db
from vimage.helpers.utils import *


class GetPoster(db.Model):
    """
        海报生成
    """

    __tablename__ = 'getposter'

    id = db.Column(db.Integer, primary_key=True)
    poster_url = db.Column(db.String(), nullable=True)

    created_at = db.Column(db.Integer, default=timestamp())
    updated_at = db.Column(db.Integer, default=timestamp(), onupdate=timestamp)

    def to_json(self):
        """
            JSON 格式化
        """

        json_post = {
            "data": {
                "poster_url": self.poster_url
            },
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "status": custom_status(message='上传成功')
        }

        return json_post

    def __repr__(self):
        return '<GetPoster {}>'.format(self.id)
