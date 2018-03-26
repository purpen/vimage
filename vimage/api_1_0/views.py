# -*- coding: utf-8 -*-
"""
    views.py

    :copyright: (c) 2018 by purpen.
"""
import json
from flask import request, abort, g, url_for, jsonify
from . import api
from ..helpers.utils import *
from ..helpers.image import *
from ..models import imageset


@api.route('/goods/wxa', methods=['POST'])
def get_wxa_poster():
    """
        获取生成的商品小程序码海报
    """

    post_data = request.get_json()

<<<<<<< HEAD

@api.route('/card/goods', methods=['POST'])
def get_goods_card():
=======
>>>>>>> origin/master
    """
    接收的数据，各参数含义：
    
    :param title: 商品标题
    :param sale_price: 商品售价
    :param brand_name: 品牌名称
    :param hint_text: 提示文字
    :param goods_img: 商品图片 url
    :param logo_img: logo图片 url
    :param qr_code_img: 二维码图片 url
    """

    data = {
        'title': post_data.get('title'),
        'sale_price': post_data.get('sale_price'),
        'brand_name': post_data.get('brand_name'),
        'hint_text': post_data.get('hint_text'),
        'goods_img': post_data.get('goods_img'),
        'logo_img': post_data.get('logo_img'),
        'qr_code_img': post_data.get('qr_code_img')
    }

    result_image_url = create_poster(data, PosterClass.GoodsInfoWxa, 0)

    return jsonify({'image_url': result_image_url})


@api.route('/goods/sales', methods=['POST'])
def get_sales_poster():
    """
        获取生成的商品促销海报
    """

    post_data = request.get_json()

    """
    接收的数据，各参数含义：
    
    :param sales_title: 促销标题
    :param sales_pct: 促销折扣百分比
    :param sales_info: 促销信息
    :param sales_brand: 促销品牌/店铺名
    :param sales_time: 促销时间
    :param hint_text: 提示文字
    :param background_img: 背景图片 url
    :param qr_code_img: 二维码图片 url
    """

    data = {
        'sales_title': post_data.get('sales_title'),
        'sales_pct': post_data.get('sales_pct'),
        'sales_info': post_data.get('sales_info'),
        'sales_brand': post_data.get('sales_brand'),
        'sales_time': post_data.get('sales_time'),
        'hint_text': post_data.get('hint_text'),
        'background_img': post_data.get('background_img'),
        'qr_code_img': post_data.get('qr_code_img')
    }

    result_image_url = create_poster(data, PosterClass.GoodsSales, 1)

    return jsonify({'image_url': result_image_url})
