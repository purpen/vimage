# -*- coding: utf-8 -*-
import enum
import string
import time
import random
import hashlib
from datetime import datetime
from string import digits, ascii_letters
from flask import jsonify, g

R200_OK = {'code': 200, 'message': 'Ok all right.'}
R201_CREATED = {'code': 201, 'message': 'All created.'}
R204_NOCONTENT = {'code': 204, 'message': 'All deleted.'}
R400_BADREQUEST = {'code': 400, 'message': 'Bad request.'}
R401_AUTHORIZED = {'code': 401, 'message': 'Unauthorized access.'}
R403_FORBIDDEN = {'code': 403, 'message': 'You can not do this.'}
R404_NOTFOUND = {'code': 404, 'message': 'No result matched.'}


def full_response(status, data, success=True):
    """
    结果响应：带数据和状态信息
    """
    return jsonify({
        'data': data,
        'status': status,
        'success': success
    })


def status_response(status, success=True):
    """
    结果响应：状态信息
    """
    return jsonify({
        'status': status,
        'success': success
    })


def custom_response(message, code=200, success=True):
    """
    结果响应：状态信息
    """
    return jsonify({
        'status': custom_status(message, code),
        'success': success
    })


def custom_status(message, code=200):
    """
    自定义状态信息
    """
    return {
        'code': code,
        'message': message
    }


def timestamp():
    """return the current timestamp as an integer."""
    return time.time()


def timestamp2string(ts, formet='%Y-%m-%d %H:%M:%S'):
    """Convert int to string."""
    return datetime.fromtimestamp(ts).strftime(formet)


def string_to_timestamp(str_value):
    """字符串日期时间转换成时间戳"""
    d = datetime.strptime(str_value, "%Y-%m-%d %H:%M:%S")
    t = d.timetuple()
    _timestamp = int(time.mktime(t))
    _timestamp = float(str(_timestamp) + str("%06d" % d.microsecond)) / 1000000

    return _timestamp


def datestr_to_timestamp(str_value):
    """字符串日期转换成时间戳"""
    dt = datetime.strptime(str_value, "%Y-%m-%d")
    return time.mktime(dt.timetuple())


class Dictate(object):
    """Object view of a dict, updating the passed in dict when values are set
        or deleted. "Dictate" the contents of a dict...: """

    def __init__(self, d):
        # since __setattr__ is overridden, self.__dict = d doesn't work
        object.__setattr__(self, '_Dictate__dict', d)

    # Dictionary-like access / updates
    def __getitem__(self, name):
        value = self.__dict[name]
        if isinstance(value, dict):  # recursively view sub-dicts as objects
            value = Dictate(value)
        return value

    def __setitem__(self, name, value):
        self.__dict[name] = value

    def __delitem__(self, name):
        del self.__dict[name]

    # Object-like access / updates
    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        del self[name]

    def __repr__(self):
        return "%s(%r)" % (type(self).__name__, self.__dict)

    def __str__(self):
        return str(self.__dict)


class MixGenId(object):
    """
    生成各种sn/sku
    """

    @staticmethod
    def gen_digits(length=7):
        """生成数字串"""
        return ''.join(random.sample(string.digits, length))

    @staticmethod
    def gen_letters(length=20):
        """生成字符串"""
        return ''.join(random.sample(string.ascii_letters, length))

    @staticmethod
    def gen_banner_sn(length=8):
        """生成banner sn"""
        prefix = 'Ad'
        return ''.join([prefix, MixGenId.gen_digits(length)])

    @staticmethod
    def gen_templet_sn(length=6):
        """生成模板编号"""
        prefix = 'T'
        return ''.join([prefix, MixGenId.gen_digits(length)])

    @staticmethod
    def gen_image_sn(length=6):
        """生成图片编号"""
        prefix = 'I'
        return ''.join([prefix, MixGenId.gen_digits(length)])

    @staticmethod
    def gen_user_xid(length=10):
        prefix = '1'
        return ''.join([prefix, MixGenId.gen_digits(length)])
