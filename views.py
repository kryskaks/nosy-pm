# -*- coding: utf8 -*-
from datetime import datetime
import json
from functools import wraps
from flask import render_template, request, redirect, url_for, jsonify, session, flash, make_response
from nosypm import app
import constants
from models import User, Merchant
from controllers import LoginController, BalanceController, FindInvoiceController
from datetime import datetime
from forms import LoginForm, InvoiceForm
import helpers

def can_you(func):
	@wraps(func)
	def wrapper(*args, **kwds):
		uid = session.get("uid", None)
		if not uid:
			#return render_template("login.html", login_form = LoginForm(), referrer = url_for(func.__name__, *args, **kwds))
			return redirect(url_for("login"))

		user = User.get_by_id(session.get("uid"))
		return func(user = user, *args, **kwds)
	return wrapper

@app.route('/login', methods = ["POST", "GET"])
def login():
	if request.method == "GET":
		return render_template("login.html", login_form = LoginForm(), referrer = None)		

	response = LoginController().call(request.form.get("login", ""), request.form.get("password", ""), session)
	if response.result != constants.ControllerResult.Ok:
		flash("Error logging in: %s" % response.message )
		return redirect(url_for("login"))

	return redirect(url_for("index", user = response.data))

@app.route('/logout')
@can_you
def logout(user):
	session.pop("uid", None)
	return render_template("login.html", login_form = LoginForm(), referrer = request.referrer)

@app.route('/')
@can_you
def index(user):	
	return render_template("index.html", user = user)

@app.route('/balance')
@can_you
def balance(user):
	response = BalanceController(user).call()
	if response.result != constants.ControllerResult.Ok:
		flash(response.message)
		return redirect(url_for("index")) 	
	map(lambda b: b.update({"Currency": helpers.CurrencyHelper.get_currency_desc(b["CurrencyId"])}), response.data)
	return render_template("balance.html", balances = response.data, user = user)

@app.route('/invoice', methods = ["GET", "POST"])
@can_you
def find_invoice(user):
	if request.method == "GET":
		return render_template("invoice.html", user = user, invoice_form = InvoiceForm(), result = None)
	response = FindInvoiceController(user).call(request.form.get("invoice_id", ""), request.form.get("order_id", ""))
	if response.result != constants.ControllerResult.Ok:
		flash(response.message)
		return redirect(url_for("find_invoice"))
	return render_template("invoice.html", user = user, invoice_form = InvoiceForm(), result = response.data)
	
@app.route('/transfer', methods = ["GET", "POST"])
@can_you
def find_transfer(user):
	return 'Transfer for %s' % user


