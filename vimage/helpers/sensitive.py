# -*- coding: utf-8 -*-
import os
import base64
from vimage.models.sensitive import Sensitive
from vimage.helpers.ocr import *


sensitive_type = {
    '1': '广告违禁词',
    '2': '敏感词'
}


class PickSensitive:
    """
        敏感信息过滤
    """

    def __init__(self, text=None, image=None, image_url=None):
        self.text = text or ''  # 需要检测的文字
        self.result_text = ''  # 过滤完毕的文字
        self.image_base64 = image  # 需要检测的图片数据 base64
        self.image_url = image_url  # 需要检测的图片url
        self.type = 1  # 敏感词类型，1：广告词 / 2：敏感词
        self.sensitive_words = list()  # 敏感词列表
        self.result_words = list()  # 检测到的敏感词列表

        self.load_sensitive_words()

    def load_sensitive_words(self):
        """
            加载敏感词库
        """

        sensitive_words = Sensitive.query.all()

        for sensitive in sensitive_words:
            self.sensitive_words.append(sensitive.word.strip())

    def filter_words(self, filter_text):
        """
            过滤敏感词
        """

        self.result_text = filter_text

        for word in self.sensitive_words:
            if word in self.result_text:
                self.result_text = self.result_text.replace(word, len(word) * '*')

                sensitive_word = Sensitive.query.filter_by(word=word).first()
                word_type_dict = {
                    'type': sensitive_type.get(str(sensitive_word.type)),
                    'text': word
                }
                self.result_words.append(word_type_dict)

        return _result_format_json(self.result_text, self.result_words)

    def filter_text(self):
        """
            过滤敏感文字
        """

        return self.filter_words(filter_text=self.text)

    def filter_image(self):
        """
            过滤敏感图片
        """

        image_text = ''

        # OCR 识别图片获取到的文字内容
        if self.image_url is not None:
            image_text = ocr_url_image(self.image_url)

        return self.filter_words(filter_text=image_text)


def _result_format_json(result_text, result_list):
    """
    格式化返回信息

    :param result_text: 过滤后的文字
    :param result_list: 检测到的文字
    :return: json格式数据
    """

    data = {'result_text': result_text,
            'words': result_list}

    return data


def _base64_convert_image(image_base64):
    """
    base64 转换成图片
    :param image_base64: 图片base64数据
    :return: 图片
    """

    if image_base64 is None:
        return {
            'error': 'base64 为空'
        }

    image = open('', 'w')
    image.write(base64.b64decode(image_base64))
    image.close()

    return image_file
