# -*- coding: utf-8 -*-
"""
    views.py

    :copyright: (c) 2018 by purpen.
"""
from flask import request, abort, g, url_for

from .. import db
from . import api
from vimage.helpers.utils import *


@api.route('/demo')
def demo():
    """测试示例"""
    resp = jsonify({'error': False})
    # 跨域设置
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
