#coding:utf-8

"""
	author	: linkin
	date	: 2019.03.02
	email	: yooleak@outlook.com

"""
import copy
import json
from settings import *
from decorator.user import *
from util.http import send_request
from core.log import getLogger
from util import from_pattern,md5

logger = getLogger(__name__)

class User:

	def __init__(self,
		username=OFFICIAL_USER,
		instagram=None,
		session=None,
		db=None,
		query_id=None,
		marked_id=None,
		fans_hash=None,
		following_hash=None,
		comment_hash=None,
		channel_hash=None,
		page_hash=None,
		tv_hash=None,
		app_id = None,
		web_app_id=None,
		tag_hash=None,
		liker_hash=None,
		comment_liker_hash=None,
		following_tag_hash=None,
		rhx_gis=None):
		self.name = username
		self._rhx_gis = rhx_gis
		self._app_id = app_id
		self._query_id = query_id
		self._marked_id = marked_id
		self._tv_hash = tv_hash
		self._channel_hash = channel_hash
		self._page_hash = page_hash
		self._fans_hash = fans_hash
		self._tag_hash = tag_hash
		self._liker_hash = liker_hash
		self._comment_hash = comment_hash
		self._following_hash = following_hash
		self._following_tag_hash = following_tag_hash
		self._comment_liker_hash = comment_liker_hash
		self._web_app_id = web_app_id
		self._posts_count = None
		self._fans_count = None
		self._following_count = None
		self._channel_posts_count = None
		self._biography = None
		self._person_page = None
		self._fullname = None
		self._homepage = None
		self._profiles = None
		self._info = None
		self._queryIds = None
		self._Id = None
		self._picture = None
		self._queryHashs = None
		self.db = db
		self.session = session 
		self.instagram = instagram
		self.url = API_USER_HOME.format(username=username)

	@property
	def Id(self):
		return self._Id if self._Id else self.get_id()

	@property
	def fans_count(self):
		return self._fans_count if self._fans_count else self.get_fans_count()

	@property
	def following_count(self):
		return self._following_count if self._following_count else self.get_following_count()

	@property
	def channel_posts_count(self):
		return self._channel_posts_count if self._channel_posts_count else self.get_channel_posts_count()
	
	@property
	def biography(self):
		return self._biography if self._biography else self.get_biography()

	@property
	def picture(self):
		return self._picture if self._picture else self.get_picture()

	@property
	def person_page(self):
		return self._person_page if self._person_page else self.get_person_page()

	@property
	def app_id(self):
		return self._app_id if self._app_id else self.get_app_id()

	@property
	def web_app_id(self):
		return self._web_app_id if self._web_app_id else self.get_web_app_id()
	
	@property
	def query_id(self):
		return self._query_id if self._query_id else self.get_query_id()

	@property
	def marked_id(self):
		return self._marked_id if self._marked_id else self.get_marked_id()

	@property
	def channel_hash(self):
		return self._channel_hash if self._channel_hash else self.get_channel_hash()
	
	@property
	def fans_hash(self):
		return self._fans_hash if self._fans_hash else self.get_fans_hash()

	@property
	def tag_hash(self):
		return self._tag_hash if self._tag_hash else self.get_tag_hash()

	@property
	def liker_hash(self):
		return self._liker_hash if self._liker_hash else self.get_liker_hash()

	@property
	def comment_liker_hash(self):
		return  self._comment_liker_hash if self._comment_liker_hash else self.get_comment_liker_hash()

	@property
	def page_hash(self):
		return self._page_hash if self._page_hash else self.get_page_hash()

	@property
	def tv_hash(self):
		return self._tv_hash if self._tv_hash else self.get_tv_hash()
	
	@property
	def comment_hash(self):
		return self._comment_hash if self._comment_hash else self.get_comment_hash()
	
	@property
	def following_hash(self):
		return self._following_hash if self._following_hash else self.get_following_hash()

	@property
	def following_tag_hash(self):
		return self._following_tag_hash if self._following_tag_hash else self.get_following_tag_hash()
	
	@property 
	def homepage(self):
		return self._homepage if self._homepage else self.get_homepage()

	@property
	def info(self):
		return self._info if self._info else self.get_info()

	@property
	def fullname(self):
		return self._fullname if self._fullname else self.get_fullname()
	
	@property
	def queryIds(self):
		return self._queryIds if self._queryIds else self.get_query_ids()
	
	@property
	def queryHashs(self):
		return self._queryHashs if self._queryHashs else self.get_query_hashs()

	@property
	def posts_count(self):
		return self._posts_count if self._posts_count else self.get_posts_count()
	
	@property
	def rhx_gis(self):
		return self._rhx_gis if self._rhx_gis else self.get_rhx_gis()

	@property
	def is_private(self):
		return self.info['is_private']

	@property
	def is_myfans(self):
		return self.info['follows_viewer']
	
	def get_homepage(self,reget=False):
		if reget or not self._homepage:
			response = send_request(self.url,
				headers=COMMON_HEADERS,
				proxy=PROXY_GLOBAL)
			self._homepage = response.text
		return self._homepage

	def get_id(self):
		self._Id = self.info['id']
		return self._Id

	def get_fans_count(self):
		self._fans_count = self.info['edge_followed_by']['count']
		return self._fans_count

	def get_following_count(self):
		self._following_count = self.info['edge_follow']['count']
		return self._following_count

	def get_channel_posts_count(self):
		self._channel_posts_count = self.info['edge_felix_video_timeline']['count']
		return self._channel_posts_count

	def get_fullname(self):
		self._fullname = self.info['full_name']
		return self._fullname

	def get_biography(self):
		self._biography = self.info['biography']
		return self._biography

	def get_person_page(self):
		self._person_page = self.info['external_url']
		return self._person_page

	def get_picture(self):
		self._picture = self.info['profile_pic_url_hd']
		return self._picture

	def get_posts_count(self):
		self._posts_count = self.info['edge_owner_to_timeline_media']['count']
		return self._posts_count

	def get_query_id(self):
		self._query_id = self.queryIds[2]
		return self._query_id

	def get_marked_id(self):
		self._marked_id = self.queryIds[1]
		return self._marked_id

	def get_fans_hash(self):
		self._fans_hash = self.queryHashs[0]
		return self._fans_hash

	def get_page_hash(self):
		self._page_hash = self.queryHashs[2]
		return self._page_hash

	def get_tv_hash(self):
		self._tv_hash = self.queryHashs[3]
		return self._tv_hash

	def get_comment_hash(self):
		self._comment_hash = self.queryIds[0]
		return self._comment_hash

	def get_tag_hash(self):
		self._tag_hash = self.queryHashs[-3]
		return self._tag_hash

	def get_following_tag_hash(self):
		self._following_tag_hash = self.queryHashs[-2]
		return self._following_tag_hash

	def get_following_hash(self):
		self._following_hash = self.queryHashs[1]
		return self._following_hash

	def get_comment_liker_hash(self):
		self._comment_liker_hash = self.queryHashs[-1]
		return self._comment_liker_hash

	def get_rhx_gis(self):
		if not self._profiles:
			self.get_info()
		self._rhx_gis = self._profiles['rhx_gis']
		return self._rhx_gis

	@exists
	@already
	def get_app_id(self):
		js_url = HOST+from_pattern(self.homepage,PATTERN_APP_ID_JS)
		response = send_request(js_url,proxy=PROXY_GLOBAL)
		self._app_id = from_pattern(response.text,PATTERN_APP_ID)
		return self._app_id

	@exists
	@already
	def get_web_app_id(self):
		js_url = HOST+from_pattern(self.homepage,PATTERN_APP_ID_JS)
		response = send_request(js_url,proxy=PROXY_GLOBAL)
		self._web_app_id = from_pattern(response.text,PATTERN_WEB_APP_ID)
		return self._web_app_id

	@exists
	@already
	def get_query_ids(self):
		js_url = HOST+from_pattern(self.homepage,PATTERN_POSTS_JS)
		response = send_request(js_url,proxy=PROXY_GLOBAL)
		self._queryIds = from_pattern(response.text,PATTERN_POSTS,allget=True)
		return self._queryIds

	@exists
	@already
	def get_query_hashs(self):
		js_url = HOST+from_pattern(self.homepage,PATTERN_QUERY_JS)
		response = send_request(js_url,proxy=PROXY_GLOBAL)
		self._queryHashs = list(from_pattern(response.text,PATTERN_FANS_FOLLOW))
		pic_page_hashs = list(from_pattern(response.text,PATTERN_PICTURE_PAGE))
		tag_hash = from_pattern(response.text,PATTERN_POSTS,allget=True)
		following_tag_hash = from_pattern(response.text,PATTERN_HASHTAG,allget=True)
		comment_liker_hash = from_pattern(response.text,PATTERN_LIKER,allget=True)
		self._queryHashs.extend(pic_page_hashs+tag_hash+following_tag_hash+comment_liker_hash)
		return self._queryHashs

	@exists
	@already
	def get_liker_hash(self):
		js_url = HOST + from_pattern(self.homepage, PATTERN_APP_ID_JS)
		response = send_request(js_url, proxy=PROXY_GLOBAL)
		self._liker_hash = from_pattern(response.text,PATTERN_LIKER)
		return  self._liker_hash

	@exists
	@already
	def get_channel_hash(self):
		js_url = HOST+from_pattern(self.homepage,PATTERN_APP_ID_JS)
		response = send_request(js_url,proxy=PROXY_GLOBAL)
		self._channel_hash = from_pattern(response.text,PATTERN_CHANNEL)
		return self._channel_hash

	@exists
	@already
	def get_info(self):
		shared_data = from_pattern(self.homepage,PATTERN_SHAREDATA)
		json_data = json.loads(shared_data)
		self._profiles = json_data
		self._info = json_data['entry_data']['ProfilePage'][0]['graphql']['user']
		return self._info

	@exists
	@already
	@login_required
	@check(MONGODB['fans'])
	def get_fans(self,delay=DELAY,count=-1,save=False,path=None,tname=None):
		_count = 0
		results = []
		_check = count if count > 0 else self.fans_count
		end_cursor = ''
		logger.info(f'Total fans of user "{self.name}":{self.fans_count}.')
		while 1:
			headers = COMMON_HEADERS
			params = copy.deepcopy(FANS_PARAMS)
			params['variables'] = params['variables'].replace('%',self.Id).replace('$',end_cursor)
			params['query_hash'] = self.fans_hash
			headers['x-ig-app-id'] = self.app_id
			md5ed = md5(self.rhx_gis + ":" + params['variables'])
			headers['x-instagram-gis']=md5ed
			response = send_request(API_USER_POSTS,
				session=self.instagram.session,
				params=params,
				headers=headers,
				delay=delay,
				json=True,
				proxy=PROXY_GLOBAL)
			json_data = response.json()
			fans = json_data['data']['user']['edge_followed_by']['edges']
			page_info = json_data['data']['user']['edge_followed_by']['page_info']
			has_next_page = page_info['has_next_page']
			end_cursor = page_info['end_cursor']
			for i in fans:
				if save:
					self.db.save(i,tname=tname)
				results.append(i)
				_count += 1
				if (_count >= count or _count >= self.fans_count) and (count > 0):
					logger.info(f'[Done]The amount of crawled fans data of user "{self.name}"'
						f':{len(results)}.[Total({self.fans_count})]')
					return results
			logger.info(f'Current amount of crawled fans of user "{self.name}":{len(results)}.'
				f'[{round(len(results)/_check,4)*100 if _check else 0}%]')
			if not has_next_page:
				logger.info(f'[Done]The amount of crawled fans data of user "{self.name}"'
					f':{len(results)}.[Total({self.fans_count})]')
				break
		return results

	@exists
	@already
	@login_required
	@check(MONGODB['following'])
	def get_followings(self,delay=DELAY,count=-1,save=False,path=None,tname=None):
		_count = 0
		results = []
		_check = count if count>0 else self.following_count
		end_cursor = ''
		logger.info(f'Total followings of user "{self.name}":{self.following_count}.')
		while 1:
			headers = COMMON_HEADERS
			params = copy.deepcopy(FOLLOWINGS_PARAMS)
			params['variables'] = params['variables'].replace('%',self.Id).replace('$',end_cursor)
			params['query_hash'] = self.following_hash
			headers['x-ig-app-id'] = self.app_id
			md5ed = md5(self.rhx_gis + ":" + params['variables'])
			headers['x-instagram-gis']=md5ed
			response = send_request(API_USER_POSTS,
				session=self.instagram.session,
				params=params,
				headers=headers,
				delay=delay,
				json=True,
				proxy=PROXY_GLOBAL)
			json_data = response.json()
			followings = json_data['data']['user']['edge_follow']['edges']
			page_info = json_data['data']['user']['edge_follow']['page_info']
			has_next_page = page_info['has_next_page']
			end_cursor = page_info['end_cursor']
			for i in followings:
				if save:
					self.db.save(i,tname=tname)
				results.append(i)
				_count += 1
				if (_count >= count or _count >= self.following_count) and (count > 0):
					logger.info(f'[Done]The amount of crawled following users by user "{self.name}"'
						f':{len(results)}.[Total({self.following_count})]')
					return results
			logger.info(f'Current amount of crawled following users by user "{self.name}"'
				f':{len(results)}.[{round(len(results)/_check,4)*100 if _check else 0}%]')
			if not has_next_page:
				logger.info(f'[Done]The amount of crawled following users by user "{self.name}"'
					f':{len(results)}.[Total({self.following_count})]')
				break
		return results

	@exists
	@already
	@login_required
	@check(MONGODB['channel'])
	def get_channel_posts(self,delay=DELAY,count=-1,save=False,path=None,tname=None):
		_count = 0
		results = []
		_check = count if count > 0 else self.channel_posts_count
		top_posts_card = self.info['edge_felix_video_timeline']
		top_posts = top_posts_card['edges']
		end_cursor = top_posts_card['page_info']['end_cursor']
		headers = COMMON_HEADERS
		headers['x-ig-app-id'] = self.app_id
		for i in top_posts:
			if save:
				self.db.save(i,tname=tname)
			_count += 1
			results.append(i)
			if (_count >= count or _count >= self.channel_posts_count) and (count > 0):
				logger.info(f'[Done]The amount of crawled channel posts data of user "{self.name}":{len(results)}.'
					f'[Total({self.channel_posts_count})]')
				return results
		logger.info(f'Total channel posts of user "{self.name}":{self.channel_posts_count}.')
		while 1:
			if not end_cursor:
				logger.info(f'[Done]The amount of crawled channel posts data of user "{self.name}":{len(results)}.'
					f'[Total({self.channel_posts_count})]')
				break
			params = copy.deepcopy(CHANNEL_PARAMS)
			params['variables'] = params['variables'].replace('%',self.Id).replace('$',end_cursor)
			params['query_hash'] = self.channel_hash
			md5ed = md5(self.rhx_gis + ":" + params['variables'])
			headers['x-instagram-gis']=md5ed
			response = send_request(API_USER_POSTS,
				session=self.instagram.session,
				params=params,
				headers=headers,
				delay=delay,
				json=True,
				proxy=PROXY_GLOBAL)
			json_data = response.json()
			posts = json_data['data']['user']['edge_felix_video_timeline']['edges']
			page_info = json_data['data']['user']['edge_felix_video_timeline']['page_info']
			has_next_page = page_info['has_next_page']
			end_cursor = page_info['end_cursor']
			for i in posts:
				if save:
					self.db.save(i,tname=tname)
				results.append(i)
				_count += 1
				if (_count >= count or _count >= self.channel_posts_count) and (count > 0):
					logger.info(f'[Done]The amount of crawled channel posts data of user "{self.name}"'
						f':{len(results)}.[Total({self.channel_posts_count})]')
					return results
			logger.info(f'Current amount of crawled channel posts data of user "{self.name}"'
				f':{len(results)}.[{round(len(results)/_check,4)*100 if _check else 0}%]')
			if not has_next_page:
				logger.info(f'[Done]The amount of crawled channel posts data of user "{self.name}"'
					f':{len(results)}.[Total({self.channel_posts_count})]')
				break
		return results

	@exists
	@already
	@check(MONGODB['database'])
	def get_posts(self,delay=DELAY,count=-1,save=False,path=None,tname=None):
		_count = 0
		results = []
		_check = count if count > 0 else self.posts_count
		top_posts_card = self.info['edge_owner_to_timeline_media']
		top_posts = top_posts_card['edges']
		end_cursor = top_posts_card['page_info']['end_cursor']
		posts_query_id = self.queryIds[2]
		headers = COMMON_HEADERS
		headers['x-ig-app-id']=self.app_id
		for i in top_posts:
			if save:
				self.db.save(i,tname=tname)
			_count += 1
			results.append(i)
			if (_count >= count or _count >= self.posts_count) and (count > 0):
				logger.info(f'[Done]The length of crawled data of user "{self.name}"'
					f':{len(results)}.[Total({self.posts_count})]')
				return results
		logger.info(f'Total posts of user "{self.name}":{self.posts_count}.')
		while 1:
			if not end_cursor:
				logger.info(f'[Done]The length of crawled data of user "{self.name}"'
					f':{len(results)}.[Total({self.posts_count})]')
				break
			params = {}
			params['query_hash']=posts_query_id
			params['variables']=r'{"id":"'+self.Id+'","first":"'+\
			str(USER_POSTS_MAX)+'","after":"'+end_cursor+'"}'
			md5ed = md5(self.rhx_gis + ":" + params['variables'])
			headers['x-instagram-gis']=md5ed
			response = send_request(API_USER_POSTS,
				params=params,
				headers=headers,
				delay=delay,
				json=True,
				proxy=PROXY_GLOBAL)
			json_data = response.json()
			data = json_data['data']['user']\
			['edge_owner_to_timeline_media']['edges']
			page_info = json_data['data']['user']\
			['edge_owner_to_timeline_media']['page_info']
			for i in data:
				if save:
					self.db.save(i,tname=tname)
				results.append(i)
				_count += 1
				if (_count >= count or _count >= self.posts_count) and (count > 0):
					logger.info(f'[Done]The length of crawled data of user "{self.name}"'
						f':{len(results)}.[Total({self.posts_count})]')
					return results
			logger.info(f'Current amount of posts of user "{self.name}"'
				f':{len(results)}.[{round(len(results)/_check,4)*100 if _check else 0}%]')
			end_cursor = page_info['end_cursor']
			if not page_info['has_next_page']:
				logger.info(f'[Done]The length of crawled data of user "{self.name}"'
					f':{len(results)}.[Total({self.posts_count})]')
				break
		return results
	
	@exists
	@already
	@check(MONGODB['tagged'])
	def get_tagged_posts(self,delay=DELAY,count=-1,save=False,path=None,tname=None):
		_count = 0
		results = []
		end_cursor = ''
		while 1:
			headers = COMMON_HEADERS
			params = copy.deepcopy(CHANNEL_PARAMS)
			params['variables'] = params['variables'].replace('%',self.Id).replace('$',end_cursor)
			params['query_hash'] = self.marked_id
			headers['x-ig-app-id'] = self.app_id
			md5ed = md5(self.rhx_gis + ":" + params['variables'])
			headers['x-instagram-gis']=md5ed
			response = send_request(API_USER_POSTS,
				params=params,
				headers=headers,
				delay=delay,
				json=True,
				proxy=PROXY_GLOBAL)
			json_data = response.json()
			posts = json_data['data']['user']['edge_user_to_photos_of_you']['edges']
			page_info = json_data['data']['user']['edge_user_to_photos_of_you']['page_info']
			has_next_page = page_info['has_next_page']
			end_cursor = page_info['end_cursor']
			for i in posts:
				if save:
					self.db.save(i,tname=tname)
				results.append(i)
				_count += 1
				if _count >= count and count > 0:
					logger.info(f'[Done]The amount of crawled tagged posts by user "{self.name}":{len(results)}.')
					return results
			logger.info(f'Current amount of crawled tagged posts by user "{self.name}":{len(results)}.')
			if not has_next_page:
				logger.info(f'[Done]The amount of crawled tagged posts by user "{self.name}":{len(results)}.')
				break
		return results

# a = User('jojowayout')
# print(a.queryHashs)
# a.get_fans(save=True,tname='linkinpark_fans')
