# -*- coding: utf-8 -*-


import pytesseract
from PIL import Image
from io import BytesIO
import requests as req


def ocr_local_image():
    """
    ocr 本地图片识别测试

    :return: 识别结果
    """

    # 英文识别
    # image = Image.open('./vimage/resource/test_image/test_en.png')
    # text = pytesseract.image_to_string(image, lang='eng')

    # 数字识别
    # image = Image.open('./vimage/resource/test_image/test_number.png')
    # text = pytesseract.image_to_string(image, lang='eng')

    # 中文识别
    image = Image.open('./vimage/resource/test_image/test_name.png')
    text = pytesseract.image_to_string(image, lang='chi_sim')

    return text


def ocr_url_image(image_url):
    """
    ocr 网络图片识别测试

    :param image_url: 图片 url
    :return: 识别结果
    """

    text = ''

    # 请求网络图片
    r = req.get(image_url, stream=True)
    if r.status_code == 200:
        image = Image.open(BytesIO(r.content)).convert('RGBA')
        text = pytesseract.image_to_string(image, lang='chi_sim')

    return text

