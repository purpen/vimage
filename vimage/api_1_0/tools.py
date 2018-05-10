# -*- coding: utf-8 -*-
import io
from flask import request, url_for, abort, g, current_app

from . import api
from vimage.models import Sensitive
from vimage.helpers.utils import *
from vimage.helpers.ocr import *
from vimage.helpers import QiniuCloud, QiniuError, GifTool, PickSensitive, VideoMake, QRCodeObject


def _qiniu_upload(content, folder, key):
    """
    上传图片至云服务

    :param content: 上传的数据
    :param key: path key
    :return: 上传结果
    """

    folder = folder
    path_key = '%s/%s' % (folder, key)

    # 保存的地址
    result_url = 'https://%s/%s' % (current_app.config['CDN_DOMAIN'], path_key)

    qiniu_cloud = QiniuCloud(current_app.config['QINIU_ACCESS_KEY'], current_app.config['QINIU_ACCESS_SECRET'],
                             current_app.config['QINIU_BUCKET_NAME'])
    try:
        qiniu_cloud.upload_content(content, path_key)
    except QiniuError as err:
        current_app.logger.warn('Qiniu upload file error: %s' % str(err))

    return result_url


@api.route('/tools/pick_sensitive_word', methods=['POST'])
def pick_sensitive_word():
    """
        智能识别敏感词
    """

    post_data = request.get_json()

    """
    post 接收参数说明
    
    text: 需要检测的文字(必传)
    
    请求示例：
    {
        "text": "今天天气赵紫阳很不错啊"
    }
    """

    # 验证参数是否合法
    if not post_data or 'text' not in post_data:
        return status_response(R400_BADREQUEST, False)

    text = post_data.get('text')

    result_data = PickSensitive(text=text).filter_text()

    return full_response(R200_OK, result_data)


@api.route('/tools/pick_sensitive_image', methods=['POST'])
def pick_sensitive_image():
    """
        智能识别含敏感词的图片
    """

    post_data = request.get_json()

    """
    post 接收参数说明
    
    image: 图像数据，base64编码
    image_url: 图片完整URL
    
    image 和 image_url 二选一, 当 image 字段存在时 image_url 字段失效。（必传）
    
    请求示例：
    {
        "image_url": "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1523876386&di=1a4ccc7bb6c5a08be845e3e27920ca87&imgtype=jpg&er=1&src=http%3A%2F%2Fuploads.oh100.com%2Fallimg%2F1706%2F1505041347-0.jpg"
    }
    """

    # 验证参数是否合法
    if not post_data or 'image' not in post_data and 'image_url' not in post_data:
        return status_response(R400_BADREQUEST, False)

    image = post_data.get('image', None)
    image_url = post_data.get('image_url', None)

    result_data = PickSensitive(image=image, image_url=image_url).filter_image()

    return full_response(R200_OK, result_data)


@api.route('/tools/gif', methods=['POST'])
def make_gif():
    """
        制作 GIF 图
    """

    post_data = request.get_json()

    """
    post 接收参数说明
    
    type: 工具类型 | 1：图片合成GIF、2：视频制作GIF、3：GIF 提取帧图片、4：GIF 倒放 | (默认为 1)
    
    images: 图片数据(array，图片数量 >= 2，暂只支持 url 格式) | (type 为1时，必传)
    video: 视频数据 | (type 为2时，必传)
    gif: 原始 GIF 图，url 格式 | (type 为3、4时，必传)
    
    size: 尺寸大小(array，[宽，高]) | 默认第1张图的尺寸，非必传
    duration: 持续时间 ms | 控制GIF的播放速度，非必传
    
    ————————————
    请求示例：
    
    1:多张图片合成
    {
        "type": 1,
        "size": [200, 200],
        "duration": 500,
        "images": [
            "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1524031703&di=65c00624d713c1d5b92a9ba4af9eecb0&imgtype=jpg&er=1&src=http%3A%2F%2Fimg.mp.itc.cn%2Fupload%2F20170626%2F2b7fd024177b4f6fb72063eb64939b1e_th.jpg",
            "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1524031627&di=e3b061d654afdcedbd23173fdeba9fdd&imgtype=jpg&er=1&src=http%3A%2F%2Fimg.pconline.com.cn%2Fimages%2Fupload%2Fupc%2Ftx%2Fpcdlc%2F1612%2F07%2Fc315%2F31704629_1481111390421.jpg"
        ]
    }
    
    3:GIF 图分解
    {
        "type": 3,
        "gif": "https://kg.erp.taihuoniao.com/gif/20180411/OzuSkbtxjYZXKaDURrVp.gif"
    }
    
    4:GIF 图倒放
    {
        "type": 4,
        "gif": "https://pic2.zhimg.com/v2-8aa36918e2879f8a94cda56b7894cad5_b.gif"
    }
    """

    if not post_data or 'images' not in post_data and 'video' not in post_data and 'gif' not in post_data:
        return status_response(R400_BADREQUEST, False)

    type = post_data.get('type', 1)
    size = post_data.get('size')
    images = post_data.get('images')
    video = post_data.get('video')
    gif = post_data.get('gif')
    duration = post_data.get('duration')

    if type == 1:
        if not images or len(images) < 2:
            return custom_response('图片数量不足 2 张', 400, False)

    # 创建 GIF 工具类，生成 GIF 图
    gif_tool = GifTool(type, images, video, gif, size, duration)
    result_data = gif_tool.get_result_gif()

    return full_response(R200_OK, result_data)


@api.route('/tools/video', methods=['POST'])
def make_video():
    """
        制作视频
    """

    post_data = request.get_json()

    """
    post 接收参数说明
    
    contents: 视频展示信息内容：图片/文字等
    
    请求示例：
    {
        "contents": [
            {
                "images":[
                    "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1525493094&di=b8a30d4bef4d6a0b0d64e711bf1af7f1&imgtype=jpg&er=1&src=http%3A%2F%2Fimg.zcool.cn%2Fcommunity%2F01d9115a5965a4a80120121fd09501.jpg%401280w_1l_2o_100sh.jpg"
                    ],
                "texts":[
                    "普罗旺斯薰衣草",
                    "￥88"
                    ]
            },
            {
                "images":[
                    "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1524898435400&di=4256edfc192c317f652c2655072d31b0&imgtype=0&src=http%3A%2F%2Fimg.zcool.cn%2Fcommunity%2F01c84e59e94e91a801216a4b3ebb80.jpg%401280w_1l_2o_100sh.jpg",
                    "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1524898394497&di=1d39b1aaf43d1fe53a513d005d38f58c&imgtype=0&src=http%3A%2F%2Fimg.zcool.cn%2Fcommunity%2F01af4559e94e93a801202b0c64207e.jpg%401280w_1l_2o_100sh.jpg"
                    ],
                "texts":[
                    "地中海风情",
                    "￥128"
                    ]
            }
        ]
    }
    """

    # 验证参数是否合法
    if not post_data or 'contents' not in post_data:
        return status_response(R400_BADREQUEST, False)

    result_video = VideoMake(post_data).make_video()

    return full_response(R200_OK, result_video)


@api.route('/tools/qr_code', methods=['POST'])
def make_qr_code():
    """
        制作生成二维码
    """

    post_data = request.get_json()

    """
    post 接收参数说明
    
    type: 数据类型：1：文字/2：网址
    content: 数据内容 文字/URL （必传）
    logo_img: 是否添加logo (url)
    version: 二维码的大小 (1 —— 40)
    fill_color: 前景色 ('#000000')
    back_color: 背景色 ('#FFFFFF')
    error_correct: 容错率 (L | M | Q | H)
    box_size: 每个“盒子”有多少像素
    border: 边框大小
    """

    # 验证参数是否合法
    if not post_data or 'content' not in post_data:
        return status_response(R400_BADREQUEST, False)

    # 生成二维码
    result_img = QRCodeObject(post_data).create_qr_code()

    # 检测二维码图片是否存在
    if not result_img:
        return status_response(custom_status('请输入正确的网址', code=400))

    # 获取二维码地址
    img_content = io.BytesIO()
    result_img.save(img_content, 'png')

    # 上传到七牛
    result_url = _qiniu_upload(img_content.getvalue(), 'QRCode', QiniuCloud.gen_path_key('.png'))

    return full_response(R200_OK, {'result_url': result_url})
