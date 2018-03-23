# -*- coding: utf-8 -*-
"""
    views.py

    :copyright: (c) 2018 by purpen.
"""
import json
from flask import request, abort, g, url_for, jsonify
from . import api
from ..helpers.utils import *
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


@api.route('/goodscard', methods=['POST'])
def get_goods_card():
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

        result_data = show_goods_card(data)

        return jsonify(result_data)

    else:
        return jsonify({"code": 0, "message": "只接受 POST 请求"})


@api.route('/salescard', methods=['POST'])
def get_sales_card():
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
            'hint_text': texts['hint_text'],
            'background_img': images['background_img'],
            'logo_img': images['logo_img'],
            'qrcode_img': images['qrcode_img']
        }

        result_data = show_sales_card(data)

        return jsonify(result_data)

    else:
        return jsonify({"code": 0, "message": "只接受 POST 请求"})
