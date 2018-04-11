# -*- coding: utf-8 -*-
import requests as req
from PIL import Image, ImageSequence
from io import BytesIO
from vimage.helpers.utils import *

from flask import current_app
from vimage.helpers import QiniuCloud, QiniuError


def _download_image(url, is_convert=False, size=None):
    """
    从图片链接中下载图片

    :param url: 链接
    :param is_convert: 图片是否转换
    :param size: 尺寸
    :return: 图片
    """

    try:
        r = req.get(url)
        image = Image.open(BytesIO(r.content))

        if is_convert is True:
            image = image.convert('RGBA')

        if size is not None:
            image = image.resize(size, Image.ANTIALIAS)

    except (req.exceptions.HTTPError, req.exceptions.URLRequired):
        return custom_response('图片链接获取失败', 400, False)

    return image


class GifTool:
    """
        GIF图制作工具
    """

    def __init__(self, type, images, movie, gif, size=None, duration=None):
        """
        初始化 GIF 图类别

        :param type: 类型 1：图片合成GIF、2：视频制作GIF、3：GIF 提取帧图片、4：GIF 倒放 | (默认为 1)
        :param images: 每帧图片的集合
        :param movie: 视频地址
        :param gif: GIF 图地址
        :param size: 尺寸
        :param duration: 持续时间 ms
        """

        self.type = type or 1
        self.images = images
        self.movie = movie
        self.gif = gif
        self.size = size
        self.duration = duration or 500

        self.tools = {
            '1': self.create_images_gif(),
            '2': self.create_movie_gif(),
            '3': self.create_resolve_gif(),
            '4': self.create_reverse_gif()
        }

    def create_images_gif(self):
        """
            多张图片合成 GIF 图
        """

        if self.images is None or self.type != 1:
            return

        # 首张图片为默认
        default_image = _download_image(self.images[0], True, self.size)

        # 默认尺寸，对所有图片进行调整
        default_size = default_image.size

        images = []
        for image_url in self.images:
            im = _download_image(image_url, True, default_size)
            images.append(im)

        # GIF 图的二进制流
        gif_content = BytesIO()
        images[0].save(gif_content, 'gif', save_all=True, append_images=images[1:], duration=self.duration, loop=0)

        result = _qiniu_upload(gif_content.getvalue(), QiniuCloud.gen_path_key('.gif'))

        return {
            'gif': result
        }

    def create_movie_gif(self):
        """
            视频制作 GIF 图
        """

        return '视频制作 GIF 图'

    def create_resolve_gif(self):
        """
            分解 GIF 图为单张图片
        """

        if self.gif is None or self.type != 3:
            return

        original_gif = _download_image(self.gif, self.size)

        images = []

        # GIF图片流的迭代器
        for image in ImageSequence.Iterator(original_gif):
            image_content = BytesIO()
            image.copy().save(image_content, 'png')

            result = _qiniu_upload(image_content.getvalue(), QiniuCloud.gen_path_key())

            images.append(result)

        return {
            'gif': self.gif,
            'images': images
        }

    def create_reverse_gif(self):
        """
            GIF 图倒放
        """

        if self.gif is None or self.type != 4:
            return

        original_gif = _download_image(self.gif, self.size)

        images = []

        # GIF图片流的迭代器
        for image in ImageSequence.Iterator(original_gif):
            images.append(image.copy())

        # 倒序排列
        images.reverse()

        # GIF 图的二进制流
        gif_content = BytesIO()
        images[0].save(gif_content, 'gif', save_all=True, append_images=images[1:], duration=self.duration, loop=0)

        result = _qiniu_upload(gif_content.getvalue(), QiniuCloud.gen_path_key('.gif'))

        return {
            'gif': self.gif,
            'reverse_gif': result
        }

    def get_result_gif(self):
        """
        获取 GIF 制作的结果

        :return: 结果数据
        """

        tool_type = str(self.type)
        result = self.tools.get(tool_type)

        return result


def _qiniu_upload(content, key):
    """
    上传图片至云服务

    :param content: 上传的数据
    :param key: path key
    :return: 上传结果
    """

    folder = 'promotion'
    path_key = '%s/%s' % (folder, key)

    # 保存的地址
    result_url = 'https://%s/%s' % (current_app.config['CDN_DOMAIN'], path_key)

    qiniu_cloud = QiniuCloud(current_app.config['QINIU_ACCESS_KEY'], current_app.config['QINIU_ACCESS_SECRET'],
                             current_app.config['QINIU_BUCKET_NAME'])
    try:
        qiniu_cloud.upload_content(content, path_key)
    except QiniuError as err:
        current_app.logger.warn('Qiniu upload gif error: %s' % str(err))

    return result_url
