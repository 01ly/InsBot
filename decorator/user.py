#coding:utf-8

"""
	author	: linkin
	date	: 2019.03.02
	email	: yooleak@outlook.com

"""
from importlib import import_module
while 1:
	try:
		import_module('config')
		import_module('dbhelper')
		import_module('log')
	except Exception as e:
		import os,sys
		sys.path.append(os.sep.join(os.getcwd().split(os.sep)[:-1]))
		continue
	break

import re
from config import *
from core.dbhelper import Database
from core.log import getLogger

logger = getLogger(__name__)

def already(func):
	def wrapper(self,*args,**kwargs):
		if not self._homepage:
			self.get_homepage()
		return func(self,*args,**kwargs)
	return wrapper

def exists(func):
	def wrapper(self,*args,**kwargs):
		sharedData = re.findall(r'_sharedData = (.+?);</script>',
			self.homepage)
		if sharedData:
			return func(self,*args,**kwargs)
		else:
			raise Exception(f'User page not found,maybe there does not exist the user you are looking for.')
	return wrapper

def login_required(func):
	def wrapper(self,*args,**kwargs):
		if self.instagram is None:
			raise Exception(f'This operation need a logined Instagram API.Please login first.')
		elif not self.instagram.logined:
			self.instagram.login()
		return func(self,*args,**kwargs)
	return wrapper

def check(dbname=None):
	def outter(func):
		def wrapper(self,*arg,**kwargs):
			save = kwargs.get('save')
			tname = kwargs.get('tname')
			if self.is_private and not self.is_myfans:
					logger.info(f'User "{self.name}" is a private account and unvailable to you.')
					return 
			if save:
				if tname is None:
					logger.error('The table name for the current saving is not given.')
					logger.warn(f'Setting tname to username:{self.name}')
					kwargs['tname'] = self.name
				if not isinstance(self.db,Database):
					logger.info('Creating MongoDB object.' )
					self.db = Database(MONGODB)
				if not self.db.connected:
					logger.info(f'Connecting MongoDB..')
					self.db.connect()
					logger.info('MongoDB connected.')
				if dbname:
					self.db.use_db(dbname)
					logger.info(f'Switched database to "{dbname}".')
			return func(self,*arg,**kwargs)
		return wrapper
	return outter