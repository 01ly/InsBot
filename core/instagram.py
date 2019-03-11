#coding:utf-8

"""
	author	: linkin
	date	: 2019.03.02
	email	: yooleak@outlook.com

"""
import time
import copy
from config import *
from settings import *
from util.instagram import *
from core.user import User
from core.login import Login
from core.log import getLogger
from core.dbhelper import Database
from core.obj import BinaryImage,ImageHandler
from decorator import login_required,force_type
from decorator.instagram import check,switch,choose
from util.http import send_request
from util import md5
from urllib3 import encode_multipart_formdata

logger = getLogger(__name__)

class Instagram:

	def __init__(self,user=None,pwd=None):
		self.user = user
		self.pwd = pwd
		self.session = None
		self.Login = None
		self.current_user = None
		self.logined = False
		self.official = None
		self.user_id = None
		self._app_id = None
		self._query_id = None
		self._marked_id = None
		self._page_hash = None
		self._tv_hash = None
		self._fans_hash = None
		self._tag_hash = None
		self._liker_hash = None
		self._comment_hash = None
		self._channel_hash = None
		self._following_hash = None
		self._following_tag_hash = None
		self._comment_liker_hash = None
		self._web_app_id = None
		self._rhx_gis = None
		self.__opt__ = None
		self._info = None
		self.db = Database(MONGODB)

	def login(self,user=USERNAME,pwd=PASSWORD):
		if not (self.user and self.pwd ):
			self.user = user
			self.pwd = pwd
		self.Login = Login(self.user,self.pwd)
		self.logined = self.Login.login()
		self.session = self.Login.session
		self.user_id = self.Login.Id

	def logout(self):
		if self.logined:
			send_request(API_LOGOUT,
				method='get',
				session=self.session,
				headers=self.logined_headers,
				proxy=PROXY_GLOBAL)
			if not self.session.cookies.get_dict().get('sessionid'):
				logger.info('Logout successfully~')

	@choose(None,api=1,method='get',out=True)
	def info(self,details=False):
		if not details:
			url = API_USER_JSON_INFO.format(userId=self.user_id)
		else:
			url = API_USER_INFO.format(username=self.user)
		tips = {
			'ok':f'Get account infos successfully!',
			'failed':f'Get account infos failed.',
		}
		return {'url':url,},tips

	@property
	def app_id(self):
		return self._app_id if self._app_id else self.__get_attr('_app_id')

	@property
	def web_app_id(self):
		return self._web_app_id if self._web_app_id else self.__get_attr('_web_app_id')

	@property
	def query_id(self):
		return self._query_id if self._query_id else self.__get_attr('_query_id')

	@property
	def marked_id(self):
		return self._marked_id if self._marked_id else self.__get_attr('_marked_id')

	@property
	def page_hash(self):
		return self._page_hash if self._page_hash else self.__get_attr('_page_hash')

	@property
	def channel_hash(self):
		return self._channel_hash if self._channel_hash else self.__get_attr('_channel_hash')

	@property
	def tv_hash(self):
		return self._tv_hash if self._tv_hash else self.__get_attr('_tv_hash')

	@property
	def tag_hash(self):
		return self._tag_hash if self._tag_hash else self.__get_attr('_tag_hash')

	@property
	def liker_hash(self):
		return  self._liker_hash if self._liker_hash else self.__get_attr('_liker_hash')

	@property
	def comment_liker_hash(self):
		return  self._comment_liker_hash if self._comment_liker_hash else self.__get_attr('_comment_liker_hash')

	@property
	def following_tag_hash(self):
		return self._following_tag_hash if self._following_tag_hash else self.__get_attr('_following_tag_hash')

	@property
	def rhx_gis(self):
		return self._rhx_gis if self._rhx_gis else self.__get_attr('_rhx_gis')

	@property
	def comment_hash(self):
		return self._comment_hash if self._comment_hash else self.__get_attr('_comment_hash')

	@property
	def fans_hash(self):
		return self._fans_hash if self._fans_hash else self.__get_attr('_fans_hash')

	@property
	def following_hash(self):
		return self._following_hash if self._following_hash else self.__get_attr('_following_hash')

	@property
	def keyparams(self):
		_ = ['app_id','query_id','marked_id','following_hash','tv_hash','channel_hash',
		'fans_hash','page_hash','comment_hash','rhx_gis','web_app_id','tag_hash',
		'following_tag_hash','liker_hash','comment_liker_hash']
		return {i:getattr(self,i) for i in _}

	@property
	def logined_headers(self):
		if not self.logined:
			self.login()
		headers = self.Login.headers
		headers['x-ig-app-id'] = self.app_id
		return headers

	def get_user(self,username):
		return User(username,self)

	@choose(None,api=1,method='get',login=False,out=True)
	def get_user_info_by_id(self,user_id):
		url = API_USER_JSON_INFO.format(userId=user_id)
		tips = {
			'ok':f'Get user (id:{user_id}) infos successfully!',
			'failed':f'Get user (id:{user_id}) infos failed.',
		}
		return {'url':url},tips

	@check()
	@login_required
	def get_user_fans(self,username,delay=DELAY,count=-1,save=False,path=None,tname=None):
		_user = User(username,self)
		fans = _user.get_fans(delay=delay,count=count,save=save,path=path,tname=tname)
		return fans

	@check()
	@login_required
	def get_user_followings(self,username,delay=DELAY,count=-1,save=False,path=None,tname=None):
		_user = User(username,self)
		followings = _user.get_followings(delay=delay,count=count,save=save,path=path,tname=tname)
		return followings

	@choose('query',method='get',out=True)
	def get_following_tags(self):
		params = {
			'query_hash':self.following_tag_hash,
			'variables':'{"id":%s}'%self.user_id,
		}
		tips={
			'ok':f'Get self following tags successfully!',
			'failed':f'Get self following tags failed.'
		}
		return {'params':params},tips

	@choose('query',method='get',out=True)
	def get_user_following_tags(self,username):
		_user = self.get_user(username)
		params = {
			'query_hash':self.following_tag_hash,
			'variables':'{"id":%s}'%_user.Id,
		}
		tips={
			'ok':f'Get user "{username}" following tags successfully!',
			'failed':f'Get user "{username}" following tags failed.'
		}
		return {'params':params},tips

	@check()
	@login_required
	def get_user_channel_posts(self,username,delay=DELAY,count=-1,save=False,path=None,tname=None):
		_user = User(username,self)
		posts = _user.get_channel_posts(delay=delay,count=count,save=save,path=path,tname=tname)
		return posts

	@check()
	def get_user_posts(self,username,delay=DELAY,count=-1,save=False,path=None,tname=None):
		_user = User(username,self)
		posts = _user.get_posts(delay=delay,count=count,save=save,path=path,tname=tname)
		return posts

	@check()
	def get_user_tagged_posts(self,username,delay=DELAY,count=-1,save=False,path=None,tname=None):
		_user = User(username,self)
		posts = _user.get_tagged_posts(delay=delay,count=count,save=save,path=path,tname=tname)
		return posts

	@check(MONGODB['comments'])
	def get_page_comments(self,shortcode,delay=DELAY,count=-1,save=False,path=None,tname=None):
		results = []
		_count = 0
		page = self.get_page_info(shortcode)
		comment_card = page['graphql']['shortcode_media']['edge_media_to_comment']
		total = comment_card['count']
		page_info = comment_card['page_info']
		top_comments = comment_card['edges']
		end_cursor = page_info['end_cursor']
		has_next = page_info['has_next_page']
		headers = COMMON_HEADERS
		headers['x-ig-app-id']=self.app_id
		headers['referer'] = API_PICTURE_PAGE.format(shortcode=shortcode)
		_check = count if count > 0 else total
		for i in top_comments:
			if save:
				self.db.save(i,tname=tname)
			results.append(i)
			_count += 1
			if (_count >= count or _count >= total) and (count > 0):
				logger.info(f'[Done]Get crawled comments of page:"{shortcode}":{len(results)}.[Total({total})]')
				return results
		if not has_next:
			logger.info(f'[Done]Get crawled comments of page:"{shortcode}":{len(results)}.[Total({total})]')
			return results
		while 1:
			if not end_cursor:
				logger.info(f'[Done]Get crawled comments of page:"{shortcode}":{len(results)}.[Total({total})]')
				break
			params = copy.deepcopy(COMMENTS_PARAMS)
			params['query_hash']=self.comment_hash
			params['variables']=params['variables'].replace('$',end_cursor).replace('%',shortcode)
			md5ed = md5(self.rhx_gis + ":" + params['variables'])
			headers['x-instagram-gis']=md5ed
			response = send_request(API_USER_POSTS,
				params=params,
				headers=headers,
				delay=delay,
				proxy=PROXY_GLOBAL,
				json=True)
			json_data = response.json()
			data = json_data['data']['shortcode_media']['edge_media_to_comment']['edges']
			page_info = json_data['data']['shortcode_media']['edge_media_to_comment']['page_info']
			for i in data:
				if save:
					self.db.save(i,tname=tname)
				results.append(i)
				_count += 1
				if (_count >= count or _count >= total) and (count > 0):
					logger.info(f'[Done]Get crawled comments of page:"{shortcode}"'
						f':{len(results)}.[Total({total})]')
					return results
			logger.info(f'Current crawled comments of page "{shortcode}"'
				f':{len(results)}.[{round(len(results)/_check,4)*100  if _check else 0}%]')
			end_cursor = page_info['end_cursor']
			if not page_info['has_next_page']:
				logger.info(f'[Done]Get crawled comments of page:"{shortcode}"'
					f':{len(results)}.[Total({total})]')
				break
		return results

	@choose(None,api=1,method='get',login=False,out=True)
	def get_page_info(self,shortcode):
		url = API_ACCESS_PAGE.format(shortcode=shortcode)
		tips = {
			'ok':f'Get media page which shortcode is "{shortcode}" successfully!',
			'failed':f'Get media page which shortcode is "{shortcode}" failed.',
		}
		return {'url':url},tips

	@choose('get_recommends',method='get',login=False,out=True)
	def get_recommends_by_keyword(self,keyword):
		params = copy.deepcopy(SEARCH_PARAMS)
		params['rank_token']=random.randrange(1,10**18)/10**18
		params['query']=keyword
		tips = {
			'ok':f'Get recommends of "{keyword}" successfully!',
			'failed':f'Get recommends of "{keyword}" failed.',
		}
		return {'params':params},tips

	@check(MONGODB['under_tag'])
	def get_posts_by_tag(self,tag,delay=DELAY,top_only=True,count=-1,save=False,tname=None,path=None):
		url = API_TAG_POSTS.format(tag=tag)
		response = send_request(url,json=True)
		data = response.json()
		hashtags = data['graphql']['hashtag']
		media_posts = hashtags['edge_hashtag_to_media']
		top_posts = hashtags['edge_hashtag_to_top_posts']['edges']
		total = media_posts['count']
		current_posts = media_posts['edges']
		page_info = media_posts['page_info']
		end_cursor = page_info['end_cursor']
		has_next_page = page_info['has_next_page']
		results = []
		_count = 0
		_check = count if count > 0 else total
		headers=COMMON_HEADERS
		headers['x-ig-app-id']=self.app_id
		logger.info(f'Total posts of tag "{tag}":{total}')
		if top_only:
			for i in top_posts:
				if save:
					self.db.save(i,tname=tname)
			return top_posts
		else:
			for i in current_posts:
				_count+=1
				results.append(i)
				if (_count>=count or _count>=total) and (count>0):
					logger.info(f'[Done]Total crawled posts of tag "{tag}":{len(results)}')
					return results
				if save:
					self.db.save(i,tname=tname)
		while 1:
			if not has_next_page:
				return results
			params = copy.deepcopy(TAG_PARAMS)
			params['query_hash']=self.tag_hash
			params['variables']=params['variables'].replace('$',tag).replace('%',end_cursor)
			md5ed = md5(self.rhx_gis + ":" + params['variables'])
			headers['x-instagram-gis']=md5ed
			response = send_request(API_USER_POSTS,
				params=params,
				delay=delay,
				headers=headers,
				json=True)
			data = response.json()
			hashtags = data['data']['hashtag']
			media_posts = hashtags['edge_hashtag_to_media']
			current_posts = media_posts['edges']
			page_info = media_posts['page_info']
			end_cursor = page_info['end_cursor']
			has_next_page = page_info['has_next_page']
			logger.info(f'Amount of current crawled posts of tag "{tag}"'
				f':{len(results)}.[{round(len(results)/_check,4)*100 if _check else 0}%]')
			for i in current_posts:
				_count+=1
				results.append(i)
				if (_count>=count or _count>=total) and (count>0):
					logger.info(f'[Done]Total crawled posts of tag "{tag}":{len(results)}')
					return results
				if save:
					self.db.save(i,tname=tname)

	@switch('follow_tag',mode='tag')
	def follow_tag(self,tag):
		res = self.__opt__
		if res and res['status'] == 'ok':
			logger.info(f'Follow tag "{tag}" successfully!')
		else:
			logger.info(f'Follow tag "{tag}" failed!')

	@switch('unfollow_tag',mode='tag')
	def unfollow_tag(self,tag):
		res = self.__opt__
		if res and res['status'] == 'ok':
			logger.info(f'Unfollow tag "{tag}" successfully!')
		else:
			logger.info(f'Unfollow tag "{tag}" failed!')

	@switch('follow')
	def follow(self,username):
		res = self.__opt__
		if res and res['status'] == 'ok':
			logger.info(f'Follow user "{username}" successfully!')
		else:
			logger.info(f'Follow user "{username}" failed!')

	@switch('unfollow')
	def unfollow(self,username):
		res = self.__opt__
		if res and  res['status'] == 'ok':
			logger.info(f'Unfollow user "{username}" successfully!')
		else:
			logger.info(f'Unfollow user "{username}" failed!')

	@switch('block')
	def block(self,username):
		res = self.__opt__
		if res and  res['status'] == 'ok':
			logger.info(f'Block user "{username}" successfully!')
		else:
			logger.info(f'Block user "{username}" failed!')

	@switch('unblock')
	def unblock(self,username):
		res = self.__opt__
		if res and  res['status'] == 'ok':
			logger.info(f'Unblock user "{username}" successfully!')
		else:
			logger.info(f'Unblock user "{username}" failed!')

	@choose('like_media',out=True)
	def like(self,media_id=None,short_code=None):
		if not any([media_id,short_code]):
			raise Exception(f'there must be one param not None at least.')
		if not media_id:
			info = self.get_page_info(short_code)
			media_id = info.get('graphql')['shortcode_media']['id']
		url = API_PAGE_LIKE.format(pid=media_id)
		tips = {
			'ok':f'Like media (id:{media_id}) successfully!',
			'failed': f'Like media (id:{media_id}) failed!'
		}
		return {'url':url},tips

	@choose('like_media', out=True)
	def unlike(self, media_id=None, short_code=None):
		if not any([media_id, short_code]):
			raise Exception(f'there must be one param not None at least.')
		if not media_id:
			info = self.get_page_info(short_code)
			media_id = info.get('graphql')['shortcode_media']['id']
		url = API_PAGE_UNLIKE.format(pid=media_id)
		tips = {
			'ok': f'Unlike media (id:{media_id}) successfully!',
			'failed': f'Unike media (id:{media_id}) failed!'
		}
		return {'url': url}, tips

	@choose(None,api=1)
	def like_comment(self,comment_id):
		url = API_COMMENT_LIKE.format(cid=comment_id)
		tips = {
			'ok': f'Like a comment (id:{comment_id}) successfully!',
			'failed': f'Like a comment (id:{comment_id}) failed.'
		}
		return {'url': url}, tips

	@choose(None,api=1)
	def unlike_comment(self,comment_id):
		url = API_COMMENT_UNLIKE.format(cid=comment_id)
		tips = {
			'ok': f'Unlike a comment (id:{comment_id}) successfully!',
			'failed': f'Unlike a comment (id:{comment_id}) failed.'
		}
		return {'url': url}, tips

	@force_type({1:str,'to':str})
	@choose(None,api=1,out=True)
	def add_comment(self,text,media_id=None,short_code=None,to=None):
		if not any([media_id, short_code]):
			raise Exception(f'there must be one param not None in (media_id,short_code) at least.')
		if not media_id:
			info = self.get_page_info(short_code)
			media_id = info.get('graphql')['shortcode_media']['id']
		data = {
			'comment_text':text,
		}
		if to:
			data['replied_to_comment_id']=to
		url = API_ADD_COMMENT.format(mediaId=media_id)
		tips = {
			'ok':f'Add comment for media(id:{media_id}) {"to "+to if to else ""} successfully!',
			'failed': f'Add comment for media(id:{media_id}) {"to " + to if to else ""} failed!',
		}
		return {'url':url,'data':data},tips

	@switch('set_private',{'is_private':'true'})
	def set_private(self):
		res = self.__opt__
		if res and  res['status'] == 'ok':
			logger.info(f'Set your account as a private account successfully!')
		else:
			logger.info(f'Set your account as a private account failed!')

	@switch('set_private',{'is_private':'false'})
	def unset_private(self):
		res = self.__opt__
		if res and  res['status'] == 'ok':
			logger.info(f'Unset your account as a private account successfully!')
		else:
			logger.info(f'Unset your account as a private account failed!')

	@switch('set_presence',{'presence_disabled':'true'})
	def disable_presence(self):
		res = self.__opt__
		if res and  res['status'] == 'ok':
			logger.info(f'Disable your presence successfully!')
		else:
			logger.info(f'Disable your presencefailed!')

	@switch('set_presence',{'presence_disabled':'false'})
	def enable_presence(self):
		res = self.__opt__
		if res and  res['status'] == 'ok':
			logger.info(f'Enable your presence successfully!')
		else:
			logger.info(f'Enable your presencefailed!')

	@switch('set_reshare',{'disabled':'1'})
	def disable_share(self):
		res = self.__opt__
		if res and  res['status'] == 'ok':
			logger.info(f'Disable people share your story as messages successfully!')
		else:
			logger.info(f'Disable people share your story as messages failed!')

	@switch('set_reshare',{'disabled':'0'})
	def enable_share(self):
		res = self.__opt__
		if res and  res['status'] == 'ok':
			logger.info(f'Enable people share your story as messages successfully!')
		else:
			logger.info(f'Enable people share your story as messages failed!')

	@force_type({'keywords':list,'default':bool})
	@switch('set_filter')
	def set_comment_filter_keywords(self,keywords=[],default=False):
		res = self.__opt__
		if default:
			show = 'by default'
		else:
			show = f'not in default mode'
			if keywords:
				show = f':{keywords}'
		if res and  res['status'] == 'ok':
			logger.info(f'Set your comments filter keywords {show} successfully!')
		else:
			logger.info(f'Set your comments filter keywords failed!')

	@force_type({1:str})
	@choose('upload_pic')
	def upload_profile_picture(self,path_or_url):
		pic = BinaryImage(path_or_url).to_binary()
		data = {'profile_pic':('profilepic.jpg',pic,'image/jpeg')}
		encode_data = encode_multipart_formdata(data)
		headers = {
			'content-length':str(len(pic)),
			'Content-Type':encode_data[1],
		}
		tips = {
			'ok':'Upload your profile picture successfully!',
			'failed':'Upload your profile picture failed!',
		}
		return {'data':encode_data[0],'headers':headers},tips

	@force_type({1:str})
	@choose('upload_pic',api=API_UPLOAD_PHOTO)
	def upload_picture(self,path_or_url):
		pic = BinaryImage(path_or_url).to_binary()
		data = {
			'upload_id':str(int(time.time() * 1000)),
			'photo':('photo.jpg',pic,'image/jpeg'),
		}
		encode_data = encode_multipart_formdata(data)
		headers = {
			'content-length':str(len(pic)),
			'Content-Type':encode_data[1],
		}
		tips = {
			'ok':'Upload your photo successfully!',
			'failed':'Upload your photo failed!',
		}
		return {'data':encode_data[0],'headers':headers},tips

	@choose('reset_password')
	def reset_password(self,new_pwd):
		data = copy.deepcopy(PASSWORD_PARAMS)
		data['old_password']=self.pwd
		data['new_password1']=new_pwd
		data['new_password2']=new_pwd
		tips = {
			'ok':'Reset your password successfully!',
			'failed':'Reset your password failed!',
		}
		return {'data':data},tips

	@choose('upload_pic')
	def remove_profile_picture(self):
		tips = {
			'ok':'Remove your profile picture successfully!',
			'failed':'Remove your profile picture failed!',
		}
		return {'data':None,'headers':{},},tips

	@choose('get_push_info',method='get',produce=False)
	def get_push_info(self):
		res = self.__opt__
		if res and  res['status'] == 'ok':
			logger.info(f'Get push info successfully:{res["body"] if res["body"] else "0 push."}')

		else:
			logger.info(f'Get push info failed!')
		return res

	@choose('get_activity',method='get',produce=False)
	def get_activity_notify(self):
		return self.__opt__

	@choose('mark_checked',data={'timestamp':str(time.time())},produce=False)
	def mark_checked(self):
		res = self.__opt__
		if res and  res['status'] == 'ok':
			logger.info(f'mark checked successfully.')
		else:
			logger.info(f'mark checked failed!')

	@choose('location_search',method='get',callback=get_location_params)
	def search_location(self,location,latitude=None,longitude=None,fuzzy=False):
		params = copy.deepcopy(LOCATION_PARAMS)
		params['rank_token']=str(random.randrange(1,10**18)/10**18)
		params['search_query'] = location
		if latitude and longitude:
			params['latitude']=latitude
			params['longitude']=longitude
		return {'params':params,'cb_kwargs':{'fuzzy':fuzzy,'location':location}},None

	@force_type({'path_or_url':str,'caption':str})
	@choose('create_post',out=True)
	def post_photo(self,path_or_url=None,upload_id=None,caption=None):
		data = copy.deepcopy(CONFIG_PHOTO_PARAMS)
		if caption:
			data['caption']=caption
		if upload_id:
			data['upload_id']=upload_id
		else:
			img = ImageHandler(path_or_url)
			valid_path = img.to_valid_post_image_path()
			data['upload_id']=self.upload_picture(valid_path)
		tips = {
			'ok':f'Post your photo Ins successfully!',
			'failed':f'Post your photo Ins failed.',
		}
		logger.info('Posting your photo Ins...')
		return {'data':data,'http_kwargs':{'delay':DELAY}},tips

	@force_type({'path_or_url':str,'caption':str})
	@choose('create_post',api=API_CREATE_STORY,out=True)
	def post_story(self,path_or_url=None,upload_id=None,caption=None):
		data = copy.deepcopy(CONFIG_PHOTO_PARAMS)
		if caption:
			data['caption'] = caption
		if upload_id:
			data['upload_id'] = upload_id
		else:
			img = ImageHandler(path_or_url)
			valid_path = img.to_valid_post_image_path()
			data['upload_id'] = self.upload_picture(valid_path)
		tips = {
			'ok': f'Post your photo story successfully!',
			'failed': f'Post your photo story failed.',
		}
		logger.info('Posting your photo story...')
		return {'data': data, 'http_kwargs': {'delay': DELAY}}, tips

	@choose('delete',api=1)
	def delete_media(self,media_id=None,short_code=None):
		if not any([media_id, short_code]):
			raise Exception(f'there must be one param not None at least.')
		if not media_id:
			info = self.get_page_info(short_code)
			media_id = info.get('graphql')['shortcode_media']['id']
		url = API_DELETE_POSTED_MEDIA.format(mediaId=media_id)
		tips = {
			'ok':f'Delete media (id:{media_id}) successfully!',
			'failed':f'Delete media (id:{media_id}) failed.Maybe the media doesn\'t exist.',
		}
		return {'url':url},tips

	@choose('delete',api=1)
	def delete_comment(self,comment_id,media_id=None,short_code=None):
		if not any([media_id, short_code]):
			raise Exception(f'there must be one param not None in (media_id,short_code) at least.')
		if not media_id:
			info = self.get_page_info(short_code)
			media_id = info.get('graphql')['shortcode_media']['id']
		url = API_DELETE_COMMENT.format(mediaId=media_id,commentId=comment_id)
		tips = {
			'ok':f'Delete a comment of media(id:{media_id}) successfully!',
			'failed':f'Delete a comment of media(id:{media_id}) failed.'
		}
		return {'url':url},tips

	@check(MONGODB['media_liker'])
	def get_media_likers(self,short_code,save=False,count=-1,delay=DELAY,tname=None,path=None):
		_count = 0
		results = []
		end_cursor = ''
		total = 0
		_check = 0
		while 1:
			params = copy.deepcopy(MEDIA_LIKER_PARAMS)
			headers = copy.deepcopy(COMMON_HEADERS)
			params['query_hash']=self.liker_hash
			params['variables'] = params['variables'].replace('$', short_code).replace('%', end_cursor)
			md5ed = md5(self.rhx_gis + ":" + params['variables'])
			headers['x-instagram-gis']=md5ed
			response = send_request(API_USER_POSTS,
									json=True,
									delay=delay,
									headers=headers,
									params=params)
			data = response.json()
			liker_card = data['data']['shortcode_media']['edge_liked_by']
			if _count==0:
				total = liker_card['count']
				_check = count if count >0 else total
				logger.info(f'Total amount of users who liked media({short_code}) : {total}')
			likers = liker_card['edges']
			page_info = liker_card['page_info']
			end_cursor = page_info['end_cursor']
			has_next_page = page_info['has_next_page']
			logger.info(f'Current grabbed users who liked media({short_code}):{len(likers)}.[{round(len(results)/_check,4)*100}%]')
			for i in likers:
				_count += 1
				results.append(i)
				if (_count >= count or _count >= total) and (count > 0):
					logger.info(f'[Done]Total crawled users who liked media({short_code}) :{len(results)}')
					return results
				if save:
					self.db.save(i, tname=tname)
			if not has_next_page:
				logger.info(f'[Done]Total crawled users who liked media({short_code}) :{len(results)}')
				return results

	@check(MONGODB['comment_liker'])
	@login_required
	def get_comment_likers(self,comment_id,save=False,count=-1,delay=DELAY,tname=None,path=None):
		_count = 0
		results = []
		end_cursor = ''
		while 1:
			params = copy.deepcopy(COMMENT_LIKER_PARAMS)
			headers = copy.deepcopy(COMMON_HEADERS)
			params['query_hash'] = self.comment_liker_hash
			params['variables'] = params['variables'].replace('$', comment_id).replace('%', end_cursor)
			md5ed = md5(self.rhx_gis + ":" + params['variables'])
			headers['x-instagram-gis'] = md5ed
			response = send_request(API_USER_POSTS,
									session=self.session,
									json=True,
									delay=delay,
									headers=headers,
									params=params)
			data = response.json()
			liker_card = data['data']['comment']['edge_liked_by']
			likers = liker_card['edges']
			page_info = liker_card['page_info']
			end_cursor = page_info['end_cursor']
			has_next_page = page_info['has_next_page']
			logger.info(
				f'Current grabbed users who liked comment({comment_id}):{len(likers)}.')
			for i in likers:
				_count += 1
				results.append(i)
				if _count >= count  and (count > 0):
					logger.info(f'[Done]Total crawled users who liked comment({comment_id}) :{len(results)}')
					return results
				if save:
					self.db.save(i, tname=tname)
			if not has_next_page:
				logger.info(f'[Done]Total crawled users who liked comment({comment_id}) :{len(results)}')
				return results

	def discover_posts(self,save=False,delay=DELAY,count=-1,tname=None,path=None):
		pass

	def get_posts_of_location(self,location,save=False,count=-1,delay=DELAY,tname=None,path=None):
		pass

	def __get_attr(self,_property):
		if not getattr(self,_property):
			if self.official is None:
				self.official = User(instagram=self)
			setattr(self,_property,getattr(self.official,_property.lstrip('_')))
		return getattr(self,_property)

a = Instagram()
logger.info(a.info(details=True))
# d = a.get_comment_likers('17967358843242707',save=True)
# d=a.get_media_likers('BuxpYvdFtfP',count=10)
# d = a.add_comment('This is posted by InsBot.GitHub:01ly/InsBot.',short_code='BuxpYvdFtfP')
# print(d)
# a.unlike_comment('17949756184248517')
# a.delete_media(short_code='ButZGujBt8
# a.delete_comment('18042937942030371',short_code='ButuTpXhWDQ')
# print(a.get_page_info('Bux8m0DhQms'))
# print(a.unlike(short_code='ButuTpXhWDQ'))
# print(a.post_story(r'https://b-ssl.duitang.com/uploads/item/201608/13/20160813004256_ArnKB.png',caption='Posted by InsBot'))
# print(a.get_push_info())
# print(a.delete_media('1994833336505674466'))
# a.get_user_fans('linkinpark',save=True,delay=3)
# print(a.delete_media('1994419799547189563'))
# print(a.get_user_info_by_id('7022182631'))
# a.get_posts_by_tag('linkinpark',save=True,top_only=False)
# print(a.get_user_following_tags('stevenfurtick'))
# a.follow_tag('anglebaby')
# print(a.info())
# a.enable_presence()
# a.login()
# a.logout()
# c = a.post_photo(r'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1000&q=80',caption=f'Posted by InsBot at {time.ctime()}')
# print(c)
# dd = a.get_activity_notify()
# a.mark_checked()
# dd = a.search_location('NewYork')
# dd = a.upload_picture(r'D:\projects\1.jpeg')
# print(dd)
# dd=a.get_push_info()
# dd = a.get_recommends_by_keyword('nba')
# a.mark_checked()
# a.get_push_info()
# print(dd['places'])
# a.remove_profile_picture()
# a.upload_profile_picture(r'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1000&q=80')
# a.reset_password(',,')
# a.set_comment_filter_keywords(keywords=['makelove','fuckyou','gay','fuck'],default=True)
# a.unblock('kobe')
# a.follow('cba')

# cc = a.get_user('linkin')
# print(cc.following_hash,cc.following_count)
# a.get_user_fans('linkinpark',save=True)
# cc.get_followings(save=True)
# cc.get_posts(save=True)
# print(a.keyparams)
# f = a.get_page_info('But53OPBwcp')
# print(a.get_page_comments('BuMkvw2gREs'))
# aa= a.get_page_comments('O_WT0Ry2LU',count=125,save=True)
# # print(aa)
# c = a.get_user('instagram')
# c.get_channel_posts(count=105)