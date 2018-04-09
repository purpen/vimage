# -*- coding: utf-8 -*-
from flask import request, url_for, abort, g

from . import api
from vimage.models import Sensitive
from vimage.helpers.utils import *
from vimage.helpers.ocr import *
from vimage.helpers.sensitive import PickSensitive


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
