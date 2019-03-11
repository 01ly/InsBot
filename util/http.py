#coding:utf-8

"""
	author	: linkin
	date	: 2019.03.02
	email	: yooleak@outlook.com

"""
import time
import requests
from importlib import import_module
while 1:
	try:
		import_module('settings')
		import_module('log')
		import_module('config')
	except Exception as e:
		import os,sys
		sys.path.append(os.sep.join(os.getcwd().split(os.sep)[:-1]))
		continue
	break

from config import *
from core.log import getLogger

logger = getLogger(__name__)
__all__ = ['send_request']

handler = {
	429	:	f'Your requests are rate limited by instagram.com.'
		 	f'Wait for a while and set DELAY in config.py to a large amounts.'
		 	f'Or use a proxy to bypass it.',
	403	:	f'Fobidden requests.',
	404	:	f'Page is removed or doesn\'t exist.Not found.',
	500	:	f'Server error.',
	400	:	f'Posted data maybe wrong.',
}

def send_request(
				url,
				method='get',
				retries =REQUEST_FAIL_RETRY,
				session=None,
				headers=None,
				params=None,
				data=None,
				proxy=None,
				delay=0,
				files=None,
				json = False,
				**kwargs):
	if session is None:
		session = requests.Session()
	if retries < 0:
		attempt = -1
	elif retries == 0:
		attempt =1
	else:
		attempt = retries
	response = None
	while attempt != 0:
		try:
			response = getattr(session,method.lower())(url,
					headers=headers,
					params=params,
					data=data,
					proxies=proxy,
					files=files,
					**kwargs)
			time.sleep(delay)
		except Exception as e:
			logger.error(f'Request {url} :{e}')
			attempt -= 1
			logger.info(f'delay {delay}s.')
			time.sleep(delay)
			continue
		if response.status_code != 200:
			logger.error(f'[CODE:{response.status_code}]{handler[response.status_code]}')
			logger.info(f'delay {delay}s.')
			time.sleep(delay)
			attempt -= 1
			continue
		if json:
			try:
				response.json()
			except:
				logger.error(f'Response is not in a valid json format.Retrying.')
				attempt-=1
				continue
		break
	if json:
		try:
			response.json()
		except:
			logger.error(f'Response is not in a valid json format.' )
			return
	return response




