# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm as Form
from wtforms import StringField, TextAreaField, IntegerField, FloatField, SelectField, RadioField
from wtforms.validators import DataRequired, InputRequired, Length, ValidationError, optional


class TempletForm(Form):
    name = StringField('模板名称', validators=[DataRequired(message='模板名称不能为空'), Length(2, 64)])
    cover_id = IntegerField('模板图', default=0)
    type = SelectField('模板类型', choices=[(1, '商品推广码')], coerce=int, default=1)
    requirements = TextAreaField('模板要求')
    status = RadioField('状态', choices=[(1, '可用'), (-1, '禁用')], coerce=int, default=1)
