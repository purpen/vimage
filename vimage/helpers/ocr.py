# -*- coding: utf-8 -*-
import pytesseract
from PIL import Image, ImageEnhance
from io import BytesIO
import requests as req


def ocr_local_image():
    """
    ocr 本地图片识别测试

    :return: 识别结果
    """

    # 英文识别
    # images = Image.open('./vimage/resource/test_image/test_en.png')
    # text = pytesseract.image_to_string(images, lang='eng')

    # 数字识别
    # images = Image.open('./vimage/resource/test_image/test_number.png')
    # text = pytesseract.image_to_string(images, lang='eng')

    # 中文识别
    # images = Image.open('./vimage/resource/test_image/test_name.png')
    # text = pytesseract.image_to_string(images, lang='chi_sim')

    # 海报图片识别
    im = Image.open('./vimage/resource/test_image/test_poster_1.png')
    image = convert_image(im)
    image.show()

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
        image = Image.open(BytesIO(r.content)).convert('L')
        text = pytesseract.image_to_string(image, lang='chi_sim')

    return text


def convert_image(input_image):
    """
    图片转换和增强处理

    :param input_image: 输入的图片
    :return: 处理后的图片
    """

    # 1、图形灰度
    image = input_image.convert('L')
    # 2、对比度处理
    image = ImageEnhance.Contrast(image).enhance(1.5)

    return image
