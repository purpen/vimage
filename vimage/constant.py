# -*- coding: utf-8 -*-


class Colors:
    """颜色配置"""

    DEFAULT_BACKGROUND_COLOR = {
        'white': '#FFFFFF',
        'black': '#000000'
    }


class Size:
    """尺寸大小配置"""

    DEFAULT_IMAGE_SIZE = {
        'square': (750, 750),
        'horizontal_rectangle': (1334, 750),
        'vertical_rectangle': (750, 1334)
    }

    POSTER_IMAGE_SIZE = {
        'width': 750,
        'height': 1334
    }

    GOODS_VIDEO_SIZE = {
        'width': 640,
        'height': 480
    }


class Fonts:
    """字体样式"""

    DEFAULT_FONT_FAMILY = 'PingFang Regular'
    DEFAULT_FONT_ALIGN = 'left'


class ImageInfo:
    """图片相关"""

    SAVE_IMAGE_QUALITY = 90
