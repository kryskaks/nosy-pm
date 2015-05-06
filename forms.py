# -*- coding: utf8 -*-
from flask.ext.wtf import Form
from wtforms import TextField, SelectField, BooleanField, PasswordField, DateField
from wtforms.validators import Required, Length

class LoginForm(Form):
	login = TextField(u'Логин', [Required(), Length(max=150)])
  	password = PasswordField(u'Пароль', [Required(), Length(max=150)])

class UserForm(Form):
	login = TextField(u'Логин', [Required(), Length(max=150)])
	password = PasswordField(u'Пароль', [Required(), Length(max=150)])
	role = SelectField(u'Роль', [Required(), Length(max=150)])
	merchant = SelectField(u'Мерчант', [Required(), Length(max=150)])
	access_list = TextField(u'Acess list', [Required(), Length(max=150)])

class MerchantForm(Form):
	name = TextField(u'Имя', [Required(), Length(max=150)])
	contacts = TextField(u'Контакты', [Length(max=150)])
	token = TextField(u'Токен', [Length(max=150)])
