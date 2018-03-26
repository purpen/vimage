# -*- coding: utf-8 -*-
from vimage import db


__all__ = [
    'Sensitive'
]


class Sensitive(db.Model):
    """敏感词库"""

    __tablename__ = 'sensitives'

    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(32), nullable=False)

    def __repr__(self):
        return '<Sensitive {}>'.format(self.word)
