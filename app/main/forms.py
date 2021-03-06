# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField
from  ..models import User, Role


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


# 普通用户的资料编辑表
class EditProfileForm(FlaskForm):
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')


# 管理员使用的资料编辑表单
class EditProfileAdminForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(1, 64), 
                                                    Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 
                                                    'Usernames must have only letters, numbers, dots or underscores')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)  # 下拉列表'SelectField'
    name = StringField('What is your name?',validators=[DataRequired()])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        # 'SelectField'实例必须在其'choices'属性中设置各选项. (选项必须是一个由元组组成的列表)
        # 元组元素组成：选项的标识符、显示在控件中的文本字符串(角色id, 角色名)
        # 参数设置coerce=int，字段的值转换为整数，而不使用默认的字符串
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name)]  
        self.user = user

    # 验证 email
    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise validationError('Emial already register.')

    # 验证 username
    def validate_username(self, field):
        if  field.data != self.user.username and User.query.filter_by(username=field.data).first():
            raise validationError('Username already in use.')


class PostForm(FlaskForm):
    content = PageDownField("What's on your mind?", validators=[DataRequired()])
    submit = SubmitField('Submit')


class CommentForm(FlaskForm):
    body = StringField('Enter your comment', validators=[DataRequired()])
    submit= SubmitField('Submit')
