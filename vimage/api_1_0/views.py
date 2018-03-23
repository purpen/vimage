# -*- coding: utf-8 -*-
"""
    views.py

    :copyright: (c) 2018 by purpen.
"""
import json
from flask import request, abort, g, url_for, jsonify
from . import api
from ..helpers.utils import *
from ..models import getposter, goodscard, salescard
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


@api.route('/goodscard', methods=['POST'])
def getGoodsCard():
    """
        商品小程序码
    """

    if request.method == 'POST':
        texts = request.get_json().get('texts')
        images = request.get_json().get('images')

        data = {
            'title': texts['title'],
            'sale_price': texts['sale_price'],
            'brand_name': texts['brand_name'],
            'hint_text': texts['hint_text'],
            'goods_img': images['goods_img'],
            'logo_img': images['logo_img'],
            'qrcode_img': images['qrcode_img']
        }

        newPoster = goodscard.GoodsCard(**data)

        showGoodsCard(data)

        return jsonify(newPoster.to_json())

    else:
        return jsonify({"code": 0, "message": "只接受 POST 请求"})


@api.route('/salescard', methods=['POST'])
def getSalesCard():
    """
        商品促销
    """

    if request.method == 'POST':
        texts = request.get_json().get('texts')
        images = request.get_json().get('images')

        data = {
            'sales_title': texts['sales_title'],
            'sales_pct': texts['sales_pct'],
            'sales_info': texts['sales_info'],
            'sales_brand': texts['sales_brand'],
            'time_text': texts['time_text'],
            'background_img': images['background_img'],
            'logo_img': images['logo_img'],
            'qrcode_img': images['qrcode_img']
        }

        newPoster = salescard.SalesCard(**data)

        showSalesCard(data)

        return jsonify(newPoster.to_json())

    else:
        return jsonify({"code": 0, "message": "只接受 POST 请求"})
