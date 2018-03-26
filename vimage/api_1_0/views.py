# -*- coding: utf-8 -*-
"""
    views.py

    :copyright: (c) 2018 by purpen.
"""
from flask import request, abort, g, url_for, jsonify

from . import api
from vimage.helpers.utils import *
from vimage.helpers.image import *
from vimage.models import ImageSet


@api.route('/goods/wxa', methods=['POST'])
def get_wxa_poster():
    """
    获取生成的商品小程序码海报

    :param title: 商品标题
    :param sale_price: 商品售价
    :param brand_name: 品牌名称
    :param hint_text: 提示文字
    :param goods_img: 商品图片 url
    :param logo_img: logo图片 url
    :param qr_code_img: 二维码图片 url
    """

    post_data = request.get_json()

    # 验证参数是否符合规则
    if not post_data or 'title' not in post_data or 'sale_price' not in post_data:
        return status_response(R400_BADREQUEST, False)

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

    return full_response(R200_OK, {
        'image_url': result_image_url
    })


@api.route('/goods/sales', methods=['POST'])
def get_sales_poster():
    """
    获取生成的商品促销海报

    :param sales_title: 促销标题
    :param sales_pct: 促销折扣百分比
    :param sales_info: 促销信息
    :param sales_brand: 促销品牌/店铺名
    :param sales_time: 促销时间
    :param hint_text: 提示文字
    :param background_img: 背景图片 url
    :param qr_code_img: 二维码图片 url
    """

    post_data = request.get_json()

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

    return full_response(R200_OK, {
        'image_url': result_image_url
    })
