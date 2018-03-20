# -*- coding: utf-8 -*-
from vimage import db
from vimage.helpers.utils import *


class GetPoster(db.Model):
    """
        海报生成
    """

    __tablename__ = 'getposter'

    id = db.Column(db.Integer, primary_key=True)

    # 标题
    title = db.Column(db.String(30), nullable=False)
    # 副标题
    subtitle = db.Column(db.String(30), nullable=True)
    # 内容
    content = db.Column(db.Text(), nullable=True)
    # 附加内容
    add_content = db.Column(db.Text(), nullable=True)
    # 主图(url)
    main_img = db.Column(db.String(), nullable=True)
    # Logo(url)
    logo_img = db.Column(db.String(), nullable=True)
    # 二维码(url)
    qrcode_img = db.Column(db.String(), nullable=True)
    # 时间
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
                    "subtitle": self.subtitle,
                    "content": self.content,
                    "add_content": self.add_content
                },
                "images": {
                    "main_img": self.main_img,
                    "logo_img": self.logo_img,
                    "qrcode_img": self.qrcode_img
                }
            },
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "status": custom_status(message='上传成功')
        }

        return json_post

    def __repr__(self):
        return '<GetPoster {}>'.format(self.id)
