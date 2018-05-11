# -*- coding: utf-8 -*-
from enum import Enum, unique


@unique
class ImageType(Enum):
    """图片的类型"""

    Goods = 0           # 商品图
    Background = 1      # 背景
    QRCode = 2          # 二维码
    Logo = 3            # logo
    BrandIcon = 4       # 品牌头像
    Border = 5          # 边框
    Modify = 6          # 修饰
    Mask = 7            # 蒙版
    Wxacode = 8         # 小程序码
    Avatar = 9          # 头像


@unique
class TextType(Enum):
    """文字内容的类型"""

    Title = 0       # 标题
    SalePrice = 1   # 价格
    Hint = 2        # 提示
    BrandName = 3   # 品牌名称
    Info = 4        # 其他信息
    Time = 5        # 时间
    SalesTitle = 6  # 促销标题
    SalesInfo = 7   # 促销信息
    SalesPCT = 8    # 促销百分比
    SalesBrand = 9  # 促销品牌
    OtherInfo1 = 10     # 其他信息（默认显示内容）
    OtherInfo2 = 11     # 其他信息（默认显示内容）
    TotalPrice = 13     # 满减总额（默认显示内容）
    DiscountPrice = 14  # 满减减额（默认显示内容）
    SymbolPCT = 15      # 百分比符号（默认显示内容）
    SymbolOff = 16      # 减价符号（默认显示内容）


@unique
class DrawShapeType(Enum):
    """绘制图形的类型"""

    Line = 0        # 直线
    Rectangle = 1   # 矩形
