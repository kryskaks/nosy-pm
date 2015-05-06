# -*- coding: utf8 -*-
from datetime import datetime
import json
from functools import wraps
from flask import render_template, request, redirect, url_for, jsonify, session, flash, make_response
from infodesk import app
import constants
from models import User, Merchant
from controllers import CanYouController, LoginController, CreateMerchantController, CreateUserController
from datetime import datetime
from forms import LoginForm, UserForm, MerchantForm

def can_you(func):
	@wraps(func)
	def wrapper(*args, **kwds):
		uid = session.get("uid", None)
		if not uid:
			return render_template("login.html", login_form = LoginForm(), referrer = url_for(func.__name__, *args, **kwds))

		user = User.get_by_id(session.get("uid"))
		return func(user = user, *args, **kwds)
	return wrapper

@app.route('/login', methods = ["POST"])
def login():	
	response = LoginController().call(request.form.get("login", ""), request.form.get("password", ""), session)
	if response.result != constants.ControllerResult.Ok:
		flash("Error logging in: %s" % response.message )
		return redirect(url_for("login"))

	return redirect(url_for("index", user = response.data))

@app.route('/logout')
@can_you
def logout():
	session.pop("uid", None)
	return render_template("login.html", login_form = LoginForm(), referrer = request.referrer)

@app.route('/')
@can_you
def index(user):	
	return render_template("index.html", user = user)	
