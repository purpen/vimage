# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm as Form
from wtforms import StringField, TextAreaField, IntegerField, FloatField, SelectField, RadioField
from wtforms.validators import DataRequired, InputRequired, Length, ValidationError, optional


class SensitiveWordsForm(Form):
    word = StringField('文字内容', validators=[DataRequired(message='内容不能为空'), Length(1, 128)])
    type = SelectField('文字类型', choices=[(1, '广告违禁词'), (2, '敏感词')], coerce=int, default=1)
