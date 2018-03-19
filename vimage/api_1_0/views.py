# -*- coding: utf-8 -*-
"""
    views.py

    :copyright: (c) 2018 by purpen.
"""
import json
from flask import request, abort, g, url_for, jsonify
from vimage.models.getposter import GetPoster
from .. import db, config
from . import api
from vimage.helpers.utils import *
from ..models import getposter
from vimage.main.views import *


@api.route('/demo')
def demo():
    """
        测试示例
    """

    resp = jsonify({'error': False})
    # 跨域设置
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@api.route('/')
def hello_world():
    """
        默认
    """

    return 'Hello World! Api V1.0'


@api.route('/get-poster', methods=['POST'])
def get_poster():
    """
        获取海报生成数据
    """

    if request.method == 'POST':
        texts = request.get_json().get('texts')
        images = request.get_json().get('images')

        data = {
            'title': texts['title'],
            'subtitle': texts['subtitle'],
            'content': texts['content'],
            'add_content': texts['add_content'],
            'main_img': images['main_img'],
            'logo_img': images['logo_img'],
            'qrcode_img': images['qrcode_img']
        }

        newPoster = GetPoster(**data)

        showPoster(data)

        # db.session.add(newPoster)
        # db.session.commit()

        return jsonify(newPoster.to_json())

    else:
        return jsonify({"code": 0, "message": "只接受 POST 请求"})


@api.route('/goodscard', methods=['POST'])
def get_goodsCard():
    """
        生成商品宣传图
    """

    title = request.form.get('title')
    market_price = request.form.get('market_price')
    wechat_name = request.form.get('goods_name')
    goods_img = 'test_goods_img.png'
    logo_img = 'test_logo_img.png'
    qrcode_img = 'test_qrcode_img.png'

    return jsonify({'code': 0, 'message': '上传成功'})

