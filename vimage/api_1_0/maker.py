# -*- coding: utf-8 -*-
import io
from flask import request, abort, g, current_app

from . import api
from vimage.helpers import QiniuCloud, Poster, QiniuError
from vimage.helpers.utils import *
from vimage.tasks import make_wxacode_image, make_promotion_image
from vimage.helpers.style import GoodsWxaStyle, GoodsSalesStyle


@api.route('/maker/wxa_poster', methods=['POST'])
def make_wxa_poster():
    """
    生成的商品小程序码海报

    :return image_url: 海报url
    """
    post_data = request.get_json()

    current_app.logger.warn('Poster data: %s' % post_data)

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

    style_id = 0

    folder = 'wxacode'
    path_key = '%s/%s' % (folder, QiniuCloud.gen_path_key())
    # 生成图片地址
    image_url = 'https://%s/%s' % (current_app.config['CDN_DOMAIN'], path_key)

    # 1、获取样式数据
    poster_style = GoodsWxaStyle(data, style_id)
    # 2、生成海报
    poster = Poster(poster_style.get_style_data())
    poster_image = poster.make()

    # 3、获取图像二进制流
    poster_content = io.BytesIO()
    poster_image.save(poster_content, 'png')

    # 4、上传图片至云服务
    qiniu_cloud = QiniuCloud(current_app.config['QINIU_ACCESS_KEY'], current_app.config['QINIU_ACCESS_SECRET'],
                             current_app.config['QINIU_BUCKET_NAME'])
    try:
        qiniu_cloud.upload_content(poster_content.getvalue(), path_key)
    except QiniuError as err:
        current_app.logger.warn('Qiniu upload wxacode error: %s' % str(err))

    # 启动任务
    make_wxacode_image.apply_async(args=[path_key, data, style_id])

    return full_response(R200_OK, {
        'image_url': image_url
    })


@api.route('/maker/promotion_poster', methods=['POST'])
def make_sales_poster():
    """
    获取生成的商品促销海报

    :return image_url: 海报url
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

    style_id = 1

    folder = 'promotion'
    path_key = '%s/%s' % (folder, QiniuCloud.gen_path_key())
    # 生成图片地址
    image_url = 'https://%s/%s' % (current_app.config['CDN_DOMAIN'], path_key)

    # 启动任务
    make_promotion_image.apply_async(args=[path_key, data, style_id])

    return full_response(R200_OK, {
        'image_url': image_url
    })
