from infodesk import logger
from models import User, Merchant
from decimal import Decimal
from copy import deepcopy
import codecs
import os
from config import TMP_DIR
from datetime import datetime
import constants

class ControllerResponse(object):
	def __init__(self, result, data = None, message = "Ok"):
		self.result = result
		self.data = data
		self.message = message

class Controller(object):
	def __init__(self, uid = None, user = None):
		if not uid and not user:
			self.user = None		
		elif not uid:
			self.user = user
		else:
			self.user = User.get_by_id(uid)
		self.log = logger

	def call(self, *args, **kwds):
		try:
			self.log.info("User %s started %s with params: %s, %s" % (self.user, self.__class__.__name__, args, kwds))			
			data = self._call(*args, **kwds)
			self.log.info("User %s finished %s with result: %s" % (self.user, self.__class__.__name__, data))
			return ControllerResponse(constants.ControllerResult.Ok, data = data)			
		except Exception, ex:			
			self.log.exception("User %s finished %s with error" % (self.user, self.__class__.__name__))
			return ControllerResponse(constants.ControllerResult.Error, message = str(ex))						

	def _call(self):
		raise NotImplemented("_call")

class LoginController(object):
	def __init__(self):
		self.log = logger

	def call(self, username, password, session):
		try:
			self.log.info("Started login with username %s " % username)			
			data = self._call(username, password, session)
			self.log.info("Successfully finished login with username %s " % username)
			return ControllerResponse(constants.ControllerResult.Ok, data = data)			
		except Exception, ex:			
			self.log.exception("Username %s finished login with error" % username)
			return ControllerResponse(constants.ControllerResult.Error, message = str(ex))				

	def _call(self, username, password, session):		
		user = User.try_get_by_login(username)		
		if not user:
			raise Exception("Username %s not found" % username)

		if not user.verify_password(password):
			raise Exception("Invalid password for %s" % username)

		self.log.info("Session: %s" % session)
		session["uid"] = user.id
		user.last_logged_in = datetime.now()
		user.save(only = [User.last_logged_in])
		self.log.info("Session: %s" % session)
		return user