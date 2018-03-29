# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm as Form
from wtforms import StringField, TextAreaField, IntegerField, FloatField, SelectField, RadioField, BooleanField, FileField
from wtforms.validators import DataRequired, InputRequired, Length, ValidationError, optional


class ImagesForm(Form):
    image = FileField('选择图片')
    name = StringField('图片名称', validators=[Length(1, 64)])
    tags = StringField('标签', validators=[Length(1, 200)])
    description = TextAreaField('图片描述', validators=[DataRequired(message='描述不能为空'), Length(2, 64)])
    cover_id = IntegerField('封面图', default=0)
    type = SelectField('图片类型', choices=[(1, '样例'), (2, '成品图'), (3, '背景'), (4, '矢量图'), (5, '产品图')],
                       coerce=int, default=1)
    approved = BooleanField('是否审核', false_values=False)
    status = RadioField('状态', choices=[(1, '可用'), (-1, '禁用')], coerce=int, default=1)
