#coding:utf-8

"""
	author	: linkin
	date	: 2019.03.02
	email	: yooleak@outlook.com

"""
import copy
from importlib import import_module
while 1:
	try:
		import_module('settings')
		import_module('util')
		import_module('log')
		import_module('config')
	except Exception as e:
		import os,sys
		sys.path.append(os.sep.join(os.getcwd().split(os.sep)[:-1]))
		continue
	break

from config import *
from settings import *
from util.http import send_request
from core.log import getLogger

logger = getLogger(__name__)

APIS = {
			'follow'		:API_FOLLOW,
			'unfollow'		:API_UNFOLLOW,
			'block'			:API_BLOCK,
			'unblock'		:API_UNBLOCK,	
			'set_private'	:API_SET_PRIVATE,
			'set_presence'	:API_SET_PRESENCE,
			'set_reshare'	:API_SET_SHARE,
			'set_filter'	:API_SET_COMMENT_FILTER,
			'reset_password':API_CHANGE_PASSWORD,
			'upload_pic'	:API_CHANGE_PROFILE_PIC,
			'get_push_info'	:API_PUSH_INFO,
			'mark_checked'	:API_MARK_CHECKED,
			'location_search':API_GET_LOCATION,
			'create_post'	:API_CREATE_POST,
			'get_activity'	:API_ACTIVITY,
			'get_recommends':API_TOP_SEARCH,
			'follow_tag'	:API_FOLLOW_TAG,
			'unfollow_tag'	:API_UNFOLLOW_TAG,
			'query'			:API_USER_POSTS,
			'posts_by_tag'	:API_TAG_POSTS,
			'like_media'	:API_PAGE_LIKE,
		}

def switch(opt,_data=None,mode='user'):
	def outter(func):
		def wrapper(self,username=None,**kwargs):
			API = APIS[opt]
			headers = self.logined_headers
			cookies = self.session.cookies.get_dict()
			headers['x-csrftoken']=cookies['csrftoken']
			data = _data
			if username and isinstance(username,str):
				if mode=='user':
					target = self.get_user(username)
					url = API.format(userid=target.Id)
				elif mode=='tag':
					url = API.format(tag=username)
			else:
				url = API
			if opt == 'set_filter':
				if kwargs.get('default'):
					data = {'config_value':'1'}
					logger.debug(f'set comments filter to default.')
				elif kwargs.get('keywords'):
					url = API_SET_COMMENT_FILTER_kEYWORDS
					k = kwargs['keywords']
					_ = ','.join([str(i) for i in k]) if len(k) > 1 else str(k[0])+','
					data = {'keywords':_}
					logger.debug(f'set comments filter keywords to {k}.')
					send_request(API_SET_COMMENT_FILTER,
					session=self.session,
					headers=headers,
					method='post',
					data={'config_value':'0'},
					proxy=PROXY_GLOBAL)
				else:
					data = {'config_value':'0'}
					logger.debug(f'set comments filter keywords not in default mode.')
			response = send_request(url,
				session=self.session,
				headers=headers,
				method='post',
				data=data,
				proxy=PROXY_GLOBAL)
			res = response.json()
			self.__opt__=res
			if not username is None:
				ret = func(self,username)
			else:
				ret = func(self,**kwargs)
			self.__opt__ = None
			return ret 
		return wrapper
	return outter

def choose(opt,method='post',data=None,
	produce=True,api=None,params=None,callback=None,
	login=True,out=False):
	def outter(func):
		def wrapper(self,*args,**kwargs):
			url = APIS[opt] if api is None else api
			if login:
				headers = self.logined_headers
				cookies = self.session.cookies.get_dict()
				headers['x-csrftoken']=cookies['csrftoken']
			else:
				headers = copy.deepcopy(COMMON_HEADERS)
			if not produce:
				response = send_request(url,
					session=self.session,
					headers=headers,
					method=method,
					data=data,
					params=params,
					json=True,
					delay=DELAY,
					proxy=PROXY_GLOBAL)
				res = response.json()
				self.__opt__=res
				ret = func(self,*args,**kwargs)
			else:
				ret = True
				data_dict,tips = func(self,*args,**kwargs)
				url = data_dict.get('url') if data_dict.get('url') else url
				headers.update(data_dict.get('headers',{}))
				if opt=='create_post':
					headers.pop('Content-Type')
					headers.pop('content-length')
				response = send_request(url,
					session=self.session,
					headers=headers,
					method=method,
					params=data_dict.get('params',None),
					data=data_dict.get('data',None),
					proxy=PROXY_GLOBAL,
					json=True,
					delay=DELAY,
					**data_dict.get('http_kwargs',{}))
				if response is None:
					return
				res = response.json()
				if callback and callable(callback):
					cb_args = data_dict.get('cb_kwargs',{})
					return callback(self,res,**cb_args)
				if res and (res.get('status','')=='ok' or res.get('graphql')):
					if opt == 'reset_password':
						self.pwd = data_dict['data']['new_password1']
					if opt == 'upload_pic':
						if not res.get('has_profile_pic'):
							if data_dict['data']:
								if not res.get('upload_id'):
									logger.info(tips['failed'])
								else:
									logger.info(tips['ok'])
									return res.get('upload_id')
							else:
								logger.info(tips['ok'])
							return ret 
					logger.info(tips['ok'])
					if opt == 'create_post':
						logger.info(f"Posted media id:{res.get('media').get('pk')}")
						return res 
				else:
					logger.info(tips['failed'])
					logger.info(f"error:{res['message']}")
					ret = False
			self.__opt__ = None
			if out:
				return res
			return  ret
		return wrapper
	return outter

def check(dbname=None):
	def outter(func):
		def wrapper(self,*arg,**kwargs):
			save = kwargs.get('save')
			tname = kwargs.get('tname')
			if save:
				if tname is None:
					logger.error('The table name for the current saving is not given.')
					logger.warn(f'Setting tname to arg[0]:{arg[0]}')
					kwargs['tname'] = str(arg[0])
				if not self.db.connected:
					logger.info(f'Connecting MongoDB..')
					self.db.connect()
					logger.info('MongoDB connected.')
				if dbname:
					self.db.use_db(dbname)
					logger.info(f'Using database:{dbname}')
			return func(self,*arg,**kwargs)
		return wrapper
	return outter