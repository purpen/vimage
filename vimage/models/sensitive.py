# -*- coding: utf-8 -*-
from vimage import db


__all__ = [
    'Sensitive'
]


class Sensitive(db.Model):
    """广告违禁词及敏感词库"""

    __tablename__ = 'sensitives'

    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(32), nullable=False)
    # 类型：1、广告违禁词；2、敏感词；
    type = db.Column(db.SmallInteger, default=1)

    @property
    def type_label(self):
        label = ''
        if self.type == 1:
            label = '广告违禁词'

        elif self.type == 2:
            label = '敏感词'

        return label

    def __repr__(self):
        return '<Sensitive {}>'.format(self.word)
