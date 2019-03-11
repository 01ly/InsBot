#coding:utf-8

"""
	author	: linkin
	date	: 2019.03.02
	email	: yooleak@outlook.com

"""
import requests
from config import * 
from settings import *
from core.log import getLogger

logger = getLogger(__name__)

class Login:

	def __init__(self,username=USERNAME,password=PASSWORD):
		self.session = requests.Session()
		self._share_data = None
		self._headers = None
		self._params = None
		self._login_result = None
		self.logined = False
		self.Id = None
		self._user = username
		self._pwd = password

	@property
	def share_data(self):
		return self._share_data if self._share_data else self.get_share_data()

	@property
	def headers(self):
		return self._headers if self._headers else self.get_headers()

	@property
	def params(self):
		return self._params if self._params else self.get_params()
	
	def get_share_data(self,reget=False):
		if reget or not self._share_data:
			data = self.session.get(API_SHARE_DATA)
			self._share_data =  data.json()
		return self._share_data

	def get_headers(self,reget=False):
		if reget or not self._headers:
			self.get_share_data(1)
		csrftoken = self.share_data['config']['csrf_token']
		rollout_hash = self.share_data['rollout_hash']
		LOGIN_HEADERS['x-csrftoken'] = csrftoken
		LOGIN_HEADERS['x-instagram-ajax'] = rollout_hash
		self._headers = LOGIN_HEADERS
		return self._headers

	def get_params(self):
		LOGIN_PARAMS['username'] = self._user
		LOGIN_PARAMS['password'] = self._pwd
		self._params = LOGIN_PARAMS
		return self._params

	def login(self):
		logger.info('Spider is logging in.')
		response = self.session.post(API_LOGIN,
			data = self.params,
			headers = self.headers)
		self._login_result = response.json()
		logger.debug(f'login result:{self._login_result}')
		if self._login_result['authenticated'] :
			self.logined = True 
			self.Id = self._login_result['userId']
			logger.info('Login successfully.')
		else:
			logger.info('Login failed.')
		return self.logined