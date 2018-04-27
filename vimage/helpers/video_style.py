# -*- coding:utf-8 -*-
from vimage.constant import *
from vimage.helpers.video_style_format import *


class MakeVideoStyle:
    """
        生成视频的样式
    """

    def __init__(self, post_data, style_id=1):
        """
        视频初始化

        :param post_data: 接收的数据
        :param style_id: 样式 id
        """

        self.data = post_data or {}

        width = Size.GOODS_VIDEO_SIZE['width']
        height = Size.GOODS_VIDEO_SIZE['height']
        default_size = (width, height)
        self.size = self.data.get('size', default_size)      # 尺寸
        self.style_id = style_id                             # 样式标识
        self.duration = self.data.get('duration', 10)        # 持续时间(s)
        self.fps = self.data.get('fps', 24)                  # 默认帧率
        self.title = self.data.get('title', '')              # 标题
        self.sub_title = self.data.get('sub_title', '')      # 副标题

        # 内容，包含图片和图片说明信息
        self.contents = []
        self.get_video_contents()

        # 视频样式的集合
        self.styles = {'1': self.goods_video_style_1()}

    def get_video_contents(self):
        """
            获取内容数据中的图片/文字等信息
        """

        if self.data.get('contents') is None:
            return

        for content_data in self.data.get('contents'):
            if not content_data or 'images' not in content_data and 'videos' not in content_data:
                return

            images = content_data.get('images', [])
            texts = content_data.get('texts', [])
            videos = content_data.get('videos', [])

            self.contents.append({'images': images, 'texts': texts, 'videos': videos})

        return self.contents

    def goods_video_style_1(self):
        """
            商品视频样式 1
        """

        font_name = Fonts.DEFAULT_FONT_FAMILY

        result_styles = []

        for index, content in enumerate(self.contents):

            # 图片
            image_style = []

            images = content.get('images')
            image_data = format_image_data(images, self.size, False, True, False, 3)
            image_style.append(image_data)

            # 文字
            text_style = []

            texts = content.get('texts')
            for txt in texts:
                # 第一组文字为'标题'
                text_color = 'black' if index == 1 else 'red'
                text_font_size = 40 if index == 1 else 20
                text_position = (50, 100) if index == 1 else (50, 150)

                text_data = format_text_data(txt, self.size, text_color, 'transparent', font_name, text_font_size,
                                             text_position, 'label', 'center', True, 2)

                text_style.append(text_data)

            result_styles.append({'images': image_style, 'texts': text_style})

        return format_result_data(result_styles, self.size, self.fps, self.duration)

    def get_style_data(self):
        """
            获取视频样式数据
        """

        style_id = str(self.style_id)

        style_data = self.styles.get(style_id)

        return style_data
