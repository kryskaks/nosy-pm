# -*- coding: utf8 -*-
from flask.ext.wtf import Form
from wtforms import TextField, SelectField, BooleanField, PasswordField, DateField
from wtforms.validators import Required, Length

class LoginForm(Form):
	login = TextField(u'Логин', [Required(), Length(max=150)])
  	password = PasswordField(u'Пароль', [Required(), Length(max=150)])

class InvoiceForm(Form):
	invoice_id = TextField(u'InvoiceId', [Length(max=150)])
	order_id = TextField(u'OrderId', [Length(max=150)])
