# -*- coding: utf-8 -*-
import io
from flask import request, abort, g, current_app

from . import api
from vimage.helpers import QiniuCloud, Poster, QiniuError
from vimage.helpers.utils import *
from vimage.tasks import make_wxacode_image, make_promotion_image
from vimage.poster_style.poster_style import *
from vimage.poster_style.gif_style import *
from vimage.poster_style.lexi_style import *
from vimage.helpers.gif_make import GifTool


@api.route('/maker/test', methods=['POST'])
def make_test():

    post_data = request.get_json()

    # 验证参数是否符合规则
    if not post_data:
        return status_response(R400_BADREQUEST, False)

    data = {
        'image_url': post_data.get('image_url')
    }

    gif_tool = GifTool(type=5, images=data.get('image_url'))
    result_gif = gif_tool.get_result_gif()

    return full_response(R200_OK, result_gif)


@api.route('/maker/watermark', methods=['POST'])
def make_watermark_picture():
    """
        图片添加水印
    """

    post_data = request.get_json()

    # 验证参数是否符合规则
    if not post_data:
        return status_response(R400_BADREQUEST, False)

    data = {
        'image_url': post_data.get('image_url'),
    }

    folder = 'watermark'
    path_key = '%s/%s' % (folder, QiniuCloud.gen_path_key())
    # 生成图片地址
    image_url = 'https://%s/%s' % (current_app.config['THUMB_CDN_DOMAIN'], path_key)

    # 1、获取样式数据
    poster_style = WatermarkPictureStyle(data)

    # 2、生成海报
    poster = Poster(poster_style.get_default_style())
    poster_image = poster.make_poster_card()

    # 3、获取图像二进制流
    poster_content = io.BytesIO()
    poster_image.save(poster_content, 'png')

    # 4、上传图片至云服务
    qiniu_cloud = QiniuCloud(current_app.config['QINIU_ACCESS_KEY'], current_app.config['QINIU_ACCESS_SECRET'],
                             current_app.config['QINIU_BUCKET_NAME'])
    try:
        qiniu_cloud.upload_content(poster_content.getvalue(), path_key)
    except QiniuError as err:
        current_app.logger.warn('Qiniu upload watermark image error: %s' % str(err))

    return full_response(R200_OK, {
        'image_url': image_url
    })


@api.route('/maker/blurry_picture', methods=['POST'])
def make_blurry_picture():
    """
        模糊图片
    """

    post_data = request.get_json()

    # 验证参数是否符合规则
    if not post_data:
        return status_response(R400_BADREQUEST, False)

    data = {
        'image_url': post_data.get('old_path'),
        'image_width': post_data.get('image_width'),
        'image_height': post_data.get('image_height'),
        'width': post_data.get('width'),
        'height': post_data.get('height'),
        'top': post_data.get('top'),
        'left': post_data.get('left')
    }

    folder = 'blurry'
    path_key = '%s/%s' % (folder, QiniuCloud.gen_path_key())
    # 生成图片地址
    image_url = 'https://%s/%s' % (current_app.config['THUMB_CDN_DOMAIN'], path_key)

    # 1、获取样式数据
    poster_style = BlurryPictureStyle(data)

    # 2、生成海报
    poster = Poster(poster_style.get_default_style())
    poster_image = poster.make_poster_card()

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

    return full_response(R200_OK, {
        'image_url': image_url
    })


@api.route('/maker/lexi_poster', methods=['POST'])
def make_lexi_poster():
    """
        生成乐喜海报
    """

    """
    请求示例：

    {
        "type": "3",
        "brand_name": "Charles的精品杂货铺",
        "describe": "自然手繪的插畫明信片，厚磅數紙質手感佳，送\n禮跟收藏都很合適！",
        "goods_images": [
            "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1526479946&di=5cf70cc2618ac597b5e375e9546e21b9&imgtype=jpg&er=1&src=http%3A%2F%2Fstatic.kouclo.com%2Fshop%2Fuploads%2Fimuzone%2Fm7147as2kg%2Fuamytqtt4cn.jpg",
            "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1526479948&di=673378ea3732a3f5d6a4ffcdcac57b98&imgtype=jpg&er=1&src=http%3A%2F%2Fwww.ylwgift.com%2FFiles%2FProduct%2F520%2F201501060320578451-1.jpg",
            "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1526479949&di=424959022576f459c0ba27b4f8a22882&imgtype=jpg&er=1&src=http%3A%2F%2Fcbu01.alicdn.com%2Fimg%2Fibank%2F2016%2F947%2F035%2F3323530749_1802120433.jpg",
            "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1526479953&di=91b8dc18f03701b07362f27669b247e9&imgtype=jpg&er=1&src=http%3A%2F%2Fimg5q.duitang.com%2Fuploads%2Fblog%2F201411%2F21%2F20141121234846_484n5.jpeg"
        ],
        "avatar_img": "https://ss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=4195649369,2360312559&fm=27&gp=0.jpg",
        "brand_logo_img": "https://ss3.bdstatic.com/70cFv8Sh_Q1YnxGkpoWK1HF6hhy/it/u=1311958929,179260596&fm=27&gp=0.jpg",
        "nickname": "Charles",
        "wxa_code_img": "https://kg.erp.taihuoniao.com/qrcode/wxacode-wx11363b7f6fe26ac8-6157c47acb344ba43a3b345ddc21dc46.jpg",
        "title": "插画明信片-星星的悄悄話",
        "sale_price": "9.9",
        "coupon_days": "7",
        "coupon_amount": "50"
    }
    """

    post_data = request.get_json()

    current_app.logger.warn('Poster data: %s' % post_data)

    # 验证参数是否符合规则
    if not post_data:
        return status_response(R400_BADREQUEST, False)

    data = {
        'type': post_data.get('type'),
        'brand_name': post_data.get('brand_name'),
        'describe': post_data.get('describe'),
        'goods_images': post_data.get('goods_images'),
        'brand_logo_img': post_data.get('brand_logo_img'),
        'wxa_code_img': post_data.get('wxa_code_img'),
        'avatar_img': post_data.get('avatar_img'),
        'coupon_amount': post_data.get('coupon_amount', 100),
        'coupon_days': post_data.get('coupon_days', 0),
        'nickname': post_data.get('nickname'),
        'title': post_data.get('title'),
        'sale_price': post_data.get('sale_price'),
        'background_img': post_data.get('background_img'),
        'city': post_data.get('city'),
        'people_count': int(post_data.get('people_count', 16341)),
        'guess_img': post_data.get('guess_img'),
        'bonus_total_amount': post_data.get('bonus_total_amount'),
        'bonus_amount': post_data.get('bonus_amount'),
        'coupon_count': post_data.get('coupon_count', 5),
        'first_answer': post_data.get('first_answer'),
        'second_answer': post_data.get('second_answer'),
        'right_count': post_data.get('right_count'),
        'ranking': post_data.get('ranking'),
        'friends': post_data.get('friends'),
        'save_money_amount': post_data.get('save_money_amount'),
        'join_user_count': post_data.get('join_user_count', 215161),
        'tag': post_data.get('tag'),
        'original_price': post_data.get('original_price'),
        'activity_tag': post_data.get('activity_tag'),
    }

    folder = 'lexi'
    path_key = '%s/%s' % (folder, QiniuCloud.gen_path_key())
    # 生成图片地址
    image_url = 'https://%s/%s' % (current_app.config['THUMB_CDN_DOMAIN'], path_key)

    # 1、获取样式数据
    poster_style = LexiPosterStyle(data)

    # 2、生成海报
    poster = Poster(poster_style.get_style_data())
    poster_image = poster.make_goods_card()

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
    # make_wxacode_image.apply_async(args=[path_key, data, style_id])

    return full_response(R200_OK, {
        'image_url': image_url
    })


@api.route('/maker/wxa_poster', methods=['POST'])
def make_wxa_poster():
    """
        生成的商品小程序码海报
    """

    """
    请求示例：
    
    {
        "title": "卡哇 普罗旺斯超声波创意香薰加湿器\nUSB 办公室车载迷你加湿器",
        "sale_price": "88",
        "brand_name": "D3IN未来店",
        "hint_text": "",
        "goods_images": [
                "https://kg.erp.taihuoniao.com/20180315/FucRIvI9p0Ay0cqlAXtpJIvsTRhR.jpg"
            ]
        "logo_img": "https://kg.erp.taihuoniao.com/20180320/FmdRh9D1LFZLMSo1DLl2gExwHX0P.png",
        "wxa_code_img": "https://kg.erp.taihuoniao.com/qrcode/wxacode-wx11363b7f6fe26ac8-6157c47acb344ba43a3b345ddc21dc46.jpg"
    }
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
        'goods_images': post_data.get('goods_images'),
        'logo_img': post_data.get('logo_img'),
        'qr_code_img': post_data.get('qr_code_img'),
        'wxa_code_img': post_data.get('wxa_code_img')
    }

    folder = 'wxacode'
    path_key = '%s/%s' % (folder, QiniuCloud.gen_path_key())
    # 生成图片地址
    image_url = 'https://%s/%s' % (current_app.config['THUMB_CDN_DOMAIN'], path_key)

    # 1、获取样式数据
    poster_style = GoodsWxaStyle(data)

    # 2、生成海报
    poster = Poster(poster_style.get_style_data())
    poster_image = poster.make_goods_card()

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
    # make_wxacode_image.apply_async(args=[path_key, data, style_id])

    return full_response(R200_OK, {
        'image_url': image_url
    })


@api.route('/maker/promotion_poster', methods=['POST'])
def make_sales_poster():
    """
        获取生成的商品促销海报
    """
    post_data = request.get_json()

    """
    请求示例：
    
    {
        "sales_title": "今天天气很好啊",
        "sales_pct": 60,
        "sales_info": "疯  狂  大  减  价  等  你  来  ！",
        "hint_text": "扫码参加",
        "qr_code_img": "https://kg.erp.taihuoniao.com/qrcode/wxacode-wx11363b7f6fe26ac8-6157c47acb344ba43a3b345ddc21dc46.jpg"
    }
    """

    # 验证参数是否合法
    if not post_data or 'sales_title' not in post_data:
        return status_response(R400_BADREQUEST, False)

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

    style_id = 4

    folder = 'promotion'
    path_key = '%s/%s' % (folder, QiniuCloud.gen_path_key())
    # 生成图片地址
    image_url = 'https://%s/%s' % (current_app.config['THUMB_CDN_DOMAIN'], path_key)

    # 1、获取样式数据
    poster_style = GoodsSalesStyle(data, style_id)

    # 2、生成海报
    poster = Poster(poster_style.get_style_data())
    poster_image = poster.make_poster_card()

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
    # make_promotion_image.apply_async(args=[path_key, data, style_id])

    return full_response(R200_OK, {
        'image_url': image_url
    })


@api.route('/maker/saying_poster', methods=['POST'])
def make_saying_poster():
    """
        制作语录、日签海报
    """

    post_data = request.get_json()

    """
    请求示例：
    {
        "style_id": "1",
        "info": "人真正的完美不在于他们拥有什么，而在于\n他们愿意分享什么",
        "nickname": "D3IN未来店",
        "back_img": "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1526521188&di=cae0dd720e3e08fcfe115a88cf3e690a&imgtype=jpg&er=1&src=http%3A%2F%2Farticle.fd.zol-img.com.cn%2Ft_s640x2000%2Fg5%2FM00%2F0B%2F0B%2FChMkJ1lTb4GIQ8XUAADODdoHCSsAAdqKADTk4MAAM4l529.jpg",
        "avatar": "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1526637159&di=eff4c9cc5b644cb48941112c4a248ffc&imgtype=jpg&er=1&src=http%3A%2F%2Fimgtu.5011.net%2Fuploads%2Fcontent%2F20170209%2F4934501486627131.jpg",
        "qr_code": "https://kg.erp.taihuoniao.com/qrcode/wxacode-wx11363b7f6fe26ac8-6157c47acb344ba43a3b345ddc21dc46.jpg",
        "hint_text": ""
    }
    """

    if not post_data:
        return status_response(R400_BADREQUEST, False)

    folder = 'saying'
    path_key = '%s/%s' % (folder, QiniuCloud.gen_path_key())
    # 生成图片地址
    image_url = 'https://%s/%s' % (current_app.config['THUMB_CDN_DOMAIN'], path_key)

    # 1、获取样式数据
    poster_style = SayingStyle(post_data)

    # 2、生成海报
    poster = Poster(poster_style.get_style_data())
    poster_image = poster.make_poster_card()

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
    # make_promotion_image.apply_async(args=[path_key, data, style_id])

    return full_response(R200_OK, {
        'image_url': image_url
    })


@api.route('/maker/gif_poster', methods=['POST'])
def make_gif_poster():
    """
        制作 GIF 动图海报
    """

    post_data = request.get_json()

    """
    post 接收参数说明
    
    images: 图片数据(array，图片数量 >= 2，暂只支持 url 格式) | (必传)
    qr_code_img: 二维码 | (可不传)
    sales_info: 展示的内容文字 | (可不传)
    
    请求示例
    {
    "images": [
        "http://static.zara-static.cn/photos/2014/I/0/2/p/4284/212/707/2/w/1920/4284212707_2_1_1.jpg?ts=1402076633517",
        "http://static.zara-static.cn/photos/2014/I/0/2/p/4284/212/707/2/w/1920/4284212707_2_3_1.jpg?timestamp=1402076642250",
        "http://static.zara-static.cn/photos/2014/I/0/2/p/4284/212/707/2/w/1920/4284212707_2_2_1.jpg?ts=1402076637678"
        ],
    "qr_code_img": "https://kg.erp.taihuoniao.com/qrcode/wxacode-wx11363b7f6fe26ac8-6157c47acb344ba43a3b345ddc21dc46.jpg",
    "sales_info": "天然凉爽的讲究面料\n自带降温滤镜\n穿上身即是大写的 “酷” 字"
    }
    """

    # 验证参数是否合法
    if not post_data or 'images' not in post_data:
        return status_response(R400_BADREQUEST, False)

    images = post_data.get('images')

    data = {
        'qr_code_img': post_data.get('qr_code_img'),
        'sales_info': post_data.get('sales_info')
    }

    style_id = 1

    # 获取样式数据
    poster_style = GoodsGifStyle(data, style_id)

    # 生成海报
    poster = Poster(poster_style.get_style_data())
    poster_image = poster.make_poster_card()

    # 创建 GIF 工具类，生成 GIF 图
    gif_tool = GifTool(type=1, images=images)
    result_gif = gif_tool.create_gif_poster(poster_image)

    return full_response(R200_OK, result_gif)
