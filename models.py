# -*- coding: utf8 -*-
import peewee
from peewee import Model, CharField, DateTimeField, ForeignKeyField, Field, PostgresqlDatabase
from config import DATABASE_URL
from playhouse.db_url import connect
from passlib.hash import pbkdf2_sha256
from datetime import datetime

db = connect(DATABASE_URL)

class _Model(Model):
	class Meta:
		database = db

	def __repr__(self):
		data = ", ".join(["%s: %s" % (key, unicode(value).encode('utf8') if value else None) for key, value in self._data.items()])
		return "{class_name}: {{ {data} }}".format(class_name = self.__class__.__name__, data = data)

	@classmethod
	def get_by_id(cls, id):
		return cls.get(cls.id == id)

class Merchant(_Model):
	token = CharField()
	name = CharField()
	contacts = CharField(null = True)
	
	class Meta:
		db_table = "merchants"

class PasswordField(CharField):
	#db_field = 'password_hash'

	def db_value(self, password):
		return pbkdf2_sha256.encrypt(password, rounds = 200000, salt_size = 16)

	def python_value(self, value):
		return str(value)

class User(_Model):
	login = CharField(index = True, unique = True)
	password = PasswordField()	
	created = DateTimeField(default = peewee.datetime.datetime.now)
	last_logged_in = DateTimeField(null = True)
	merchant = ForeignKeyField(Merchant, null = True)
	role = CharField()
	access_list = CharField(null = True)

	@classmethod
	def get_by_login(cls, login):
		return cls.get(cls.login == login)

	@classmethod
	def try_get_by_login(cls, login):
		try:
			return cls.get_by_login(login)	
		except cls.DoesNotExist:
			db.rollback()
			return None
		except Exception, ex:
			db.rollback()
			raise ex

	class Meta:
		db_table = "users"

	def verify_password(self, password):
		return pbkdf2_sha256.verify(password, self.password)

create_tables_list = [Merchant, User]
drop_tables_list = [User, Merchant]

def create_tables():
	try:
		db.connect()
		db.create_tables(create_tables_list)
	except Exception, ex:		
		db.rollback()
		raise ex

def drop_tables():
	try:
		db.connect()
		map(lambda l: db.drop_table(l, True), drop_tables_list)
	except Exception, ex:		
		db.rollback()
		raise ex

def init_db():		
	try:
		drop_tables()
		create_tables()
		padmin = User.create(password = '123', login = 'padmin', role = 'projectAdmin')
	except Exception, ex:		
		db.rollback()
		raise

if __name__ == '__main__':
	#db.create_table(User)
	init_db()
