# -*- coding: utf-8 -*-
import io
from flask import request, url_for, abort, g, current_app

from . import api
from vimage.models import Sensitive
from vimage.helpers.utils import *
from vimage.helpers.ocr import *
from vimage.helpers.gif_make import GifTool
from vimage.helpers.video_make import *
from vimage.helpers.sensitive import PickSensitive
from vimage.helpers import QiniuCloud, QiniuError


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
    
    images: 图片完整URL
    
    请求示例：
    {
        "images": [
            "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1524659408&di=0cd528f30be918bc8d433bd52da956e0&imgtype=jpg&er=1&src=http%3A%2F%2Fpic29.nipic.com%2F20130524%2F8384088_142644789000_2.jpg",
            "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1524659427&di=b6dba0bf33d2415a525135fff23cb3ae&imgtype=jpg&er=1&src=http%3A%2F%2Fimgsrc.baidu.com%2Fimage%2Fc0%253Dshijue1%252C0%252C0%252C294%252C40%2Fsign%3D55c986aeefdde711f3df4bb5cf86a46e%2F91ef76c6a7efce1b1dbdfe61a551f3deb58f6582.jpg",
            "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1524659442&di=c151d4a86bb758aff3b67111641af309&imgtype=jpg&er=1&src=http%3A%2F%2Fimgsrc.baidu.com%2Fimage%2Fc0%253Dshijue1%252C0%252C0%252C294%252C40%2Fsign%3D4e344d757cc6a7efad2ba0659593c524%2Fcf1b9d16fdfaaf515afb6915865494eef01f7a04.jpg",
            "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1524659458&di=91be1d54d1df645dc608e0c998070f33&imgtype=jpg&er=1&src=http%3A%2F%2Fimgsrc.baidu.com%2Fimage%2Fc0%253Dshijue1%252C0%252C0%252C294%252C40%2Fsign%3D50953cc1bcfd5266b3263457c371fd5e%2Fd1160924ab18972b055930e0eccd7b899e510abc.jpg",
            "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1524659470&di=bb169087bb89d786c21dcab5c38d91c9&imgtype=jpg&er=1&src=http%3A%2F%2Fimgsrc.baidu.com%2Fimage%2Fc0%253Dshijue1%252C0%252C0%252C294%252C40%2Fsign%3D53213dc0bcfd5266b3263457c371fd5e%2Fd1160924ab18972b06ed31e1eccd7b899f510ac1.jpg"
        ]
    }
    """

    # 验证参数是否合法
    if not post_data or 'images' not in post_data:
        return status_response(R400_BADREQUEST, False)

    images = post_data.get('images', None)

    images_to_video(images)

    return full_response(R200_OK, {
        'status': 'OK'
    })
