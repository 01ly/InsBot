#coding:utf-8

"""
	author	: linkin
	date	: 2019.03.02
	email	: yooleak@outlook.com

"""

import random
from ua import USER_AGENTS

HOST = 'https://www.instagram.com'
OFFICIAL_USER = 'instagram'
IMAGE_RATIO = (0.55,1.25)

# API
## API  POST
API_LOGIN = 'https://www.instagram.com/accounts/login/ajax/'
API_SIGNUP = 'https://www.instagram.com/accounts/web_create_ajax/attempt/'
API_SEND_SMS_CODE = 'https://www.instagram.com/accounts/send_signup_sms_code_ajax/'
API_CREATE_ACCOUNT = 'https://www.instagram.com/accounts/web_create_ajax/'
API_FOLLOW = 'https://www.instagram.com/web/friendships/{userid}/follow/'
API_UNFOLLOW = 'https://www.instagram.com/web/friendships/{userid}/unfollow/'
API_FOLLOW_TAG = 'https://www.instagram.com/web/tags/follow/{tag}/'
API_UNFOLLOW_TAG = 'https://www.instagram.com/web/tags/unfollow/{tag}/'
API_BLOCK = 'https://www.instagram.com/web/friendships/{userid}/block/'
API_UNBLOCK = 'https://www.instagram.com/web/friendships/{userid}/unblock/'
API_REPORT = 'https://www.instagram.com/users/{userid}/report/'
API_SET_PRIVATE = 'https://www.instagram.com/accounts/set_private/'
API_SET_PRESENCE = 'https://www.instagram.com/accounts/set_presence_disabled/'
API_SET_SHARE = 'https://www.instagram.com/users/set_disallow_story_reshare_web/'
API_SET_COMMENT_FILTER = 'https://www.instagram.com/accounts/set_comment_filter_web/'
API_SET_COMMENT_FILTER_kEYWORDS = 'https://www.instagram.com/accounts/set_comment_filter_keywords_web/'
API_EDIT_PROFILE = 'https://www.instagram.com/accounts/edit/'
API_CHANGE_PROFILE_PIC = 'https://www.instagram.com/accounts/web_change_profile_picture/'
API_CHANGE_PASSWORD = 'https://www.instagram.com/accounts/password/change/'
API_PAGE_LIKE = 'https://www.instagram.com/web/likes/{pid}/like/'
API_PAGE_UNLIKE = 'https://www.instagram.com/web/likes/{pid}/unlike/'
API_PAGE_COMMENT = 'https://www.instagram.com/web/comments/{pid}/add/'
API_PAGE_SAVE = 'https://www.instagram.com/web/save/{pid}/save/'
API_COMMENT_LIKE = 'https://www.instagram.com/web/comments/like/{cid}/'
API_COMMENT_UNLIKE = 'https://www.instagram.com/web/comments/unlike/{cid}/'
API_ADD_COMMENT = 'https://www.instagram.com/web/comments/{mediaId}/add/'
API_DELETE_COMMENT = 'https://www.instagram.com/web/comments/{mediaId}/delete/{commentId}/'
API_UPLOAD_PHOTO = 'https://www.instagram.com/create/upload/photo/'
API_CREATE_POST = 'https://www.instagram.com/create/configure/'
API_CREATE_STORY = 'https://www.instagram.com/create/configure_to_story/'
API_MARK_CHECKED = 'https://www.instagram.com/web/activity/mark_checked/'
API_CHALLENGE = 'https://www.instagram.com/challenge/'
API_DELETE_POSTED_MEDIA = 'https://www.instagram.com/create/{mediaId}/delete/'
API_REQUEST_ONE_TAP = 'https://www.instagram.com/accounts/request_one_tap_login_nonce/'
API_MARK_SEEN = 'https://www.instagram.com/web/discover/mark_su_seen/'

## API GET
API_LOGOUT = 'https://www.instagram.com/accounts/logout/'
API_LOGIN_SYNC = 'https://www.facebook.com/instagram/login_sync/'
API_USER_JSON_INFO = 'https://i.instagram.com/api/v1/users/{userId}/info/'
API_SHARE_DATA = 'https://www.instagram.com/data/shared_data/'
API_TOP_SEARCH = 'https://www.instagram.com/web/search/topsearch/'
API_USER_POSTS = 'https://www.instagram.com/graphql/query/'
API_USER_INFO = 'https://www.instagram.com/{username}?__a=1'
API_USER_HOME = 'https://www.instagram.com/{username}/'
API_PICTURE_PAGE = 'https://www.instagram.com/p/{shortcode}/'
API_TV_PAGE = 'https://www.instagram.com/tv/{shortcode}/'
API_ACCESS_PAGE = 'https://www.instagram.com/p/{shortcode}/?__a=1'
API_PROFILE = 'https://www.instagram.com/accounts/edit/?__a=1'
API_ACTIVITY = 'https://www.instagram.com/accounts/activity/?__a=1&include_reel=true'
API_GET_LOCATION = 'https://www.instagram.com/location_search/'
API_PUSH_INFO = 'https://www.instagram.com/push/web/get_push_info'
API_GET_MID = 'https://www.instagram.com/web/__mid/'
API_TAG_POSTS = 'https://www.instagram.com/explore/tags/{tag}/?__a=1'


# HEADERS 
## COMMON HEADERS
COMMON_HEADERS = {
	'accept': '*/*',
	'accept-encoding': 'gzip, deflate, br',
	'user-agent': random.choice(USER_AGENTS),
	'x-requested-with': 'XMLHttpRequest',
}
## LOGIN HEADERS
LOGIN_HEADERS = {
	'accept': '*/*',
	'accept-encoding': 'gzip, deflate, br',
	'accept-language': 'zh-CN,zh;q=0.9',
	'content-type': 'application/x-www-form-urlencoded',
	'origin': HOST,
	'user-agent': random.choice(USER_AGENTS),
	'x-requested-with': 'XMLHttpRequest',
}

# PARAMS
## LOGIN PARAMS
LOGIN_PARAMS = {
	'queryParams': '{"source":"auth_switcher"}',
	'optIntoOneTap': 'false',
}

## EDIT ACCOUNT PROFILE PARAMS
EDIT_PARAMS = {
	'first_name':'',
	'email': '',
	'username': '',
	'phone_number': '',
	'gender': '',
	'biography': '',
	'external_url': '',
	'chaining_enabled': '',
}

## CHANGE PASSWORD PARAMS
PASSWORD_PARAMS = {
	'old_password': '',
	'new_password1': '',
	'new_password2': '',
}

## FANS REQUEST PARAMS
FANS_PARAMS = {
	'query_hash':'',
	'variables': '{"id":"%","include_reel":true,"fetch_mutual":true,"first":100,"after":"$"}',
}

## FOLLOWINGS REQUEST PARAMS
FOLLOWINGS_PARAMS = {
	'query_hash':'',
	'variables': '{"id":"%","include_reel":true,"fetch_mutual":false,"first":100,"after":"$"}',
}

## GET POSTS PARAMS
POSTS_PARAMS = {
	'query_hash': '',
	'variables': ''
}

## GET PICTURE/VIDEO PAGE PARAMS
PAGE_PARAMS = {
	'query_hash': '',
	'variables': '{"shortcode":"$","child_comment_count":3,"fetch_comment_count":40,"parent_comment_count":50,"has_threaded_comments":false}',
}

## CHANNEL POSTS PARAMS
CHANNEL_PARAMS = {
	'query_hash': '',
	'variables': '{"id":"%","first":100,"after":"$"}',
}

## GET TV PAGE PARAMS
TV_PARAMS = {
	'query_hash': '',
	'variables': '{"shortcode":"$","include_reel":true,"include_logged_out":false}',
}

## GET COMMENTS PARAMS
COMMENTS_PARAMS = {
	'query_hash': '',
	'variables': '{"shortcode":"%","first":100,"after":"$"}'
}

## GET LOCATION PARAMS
LOCATION_PARAMS = {
	'search_query': '',
	'rank_token': '',
	'latitude': '34.0434783',
	'longitude': '-118.25193139999999',
}

## CREATE NEW PHOTO POST PAMRAMS
CONFIG_PHOTO_PARAMS = {
	'upload_id': '',
	# 'caption': '',
	# 'geotag_enabled':'true',
	# 'location':'',
	# 'usertags': '',
	# 'custom_accessibility_caption': '',
	# 'retry_timeout':'' ,
}

## SEND CHALLENGE
CHALLENGE_CODE = {
	'phone_number':'',
}

## VERIFY CHALLENGE CODE
CHALLENGE_CODE_VERIFY = {
	'security_code':'',
}

## SEARCH PARAMS
SEARCH_PARAMS = {
	'context': 'blended',
	'query': '',
	'rank_token': '',
	'include_reel': 'true',
}

# GET POSTS OF TAG PARAMS
TAG_PARAMS = {
	'query_hash':'',
	'variables':'{"tag_name":"$","show_ranked":false,"first":100,"after":"%"}'
}

# GET MEDIA LIKERS PARAMS
MEDIA_LIKER_PARAMS = {
	'query_hash': '',
	'variables': '{"shortcode":"$","include_reel":true,"first":100,"after":"%"}'
}

# GET COMMENT LIKERS PARAMS
COMMENT_LIKER_PARAMS = {
	'query_hash': '',
	'variables': '{"comment_id":"$","first":24,"after":"%"}'
}

## DISCOVER USERS PARAMS
DISCOVER_USERS_PARAMS = {
	'query_hash': '',
	'variables': {
		"fetch_media_count":0,
		"fetch_suggested_count":100,
		"ignore_cache":False,
		"filter_followed_friends":True,
		"seen_ids":[],
		"include_reel":True
	},
}

# PATTERN 
## HOME USER　SHARED DATA PATTERN
PATTERN_SHAREDATA = r'_sharedData = (.+?);</script>'

## QUERY　HASH PATTERN
PATTERN_APP_ID = r"instagramWebDesktopFBAppId='(.+?)',"
PATTERN_WEB_APP_ID = r"instagramWebFBAppId='(.+?)',"
PATTERN_CHANNEL = r'USER_FELIX_MEDIA:{id:"(.+?)",'
PATTERN_PICTURE_PAGE = r';var E="(.+?)",u="(.+?)",c="(.+?)",'
PATTERN_FANS_FOLLOW = r'var t="(.+)",n="(.+)",u=1,l={inbound:o'
PATTERN_POSTS = r'queryId:"(.+?)",queryParams:f'
PATTERN_HASHTAG = r't="(.+?)";e.getHashtag'
PATTERN_POSTS_JS = r'(/static/bundles/metro/ProfilePageContainer.js/.+?\.js)'
PATTERN_QUERY_JS = r'(/static/bundles/metro/Consumer.js/.+?\.js)'
PATTERN_APP_ID_JS = r'(/static/bundles/metro/ConsumerCommons.js/.+?\.js)'
PATTERN_LIKER = r'var t="(.+)",n=[^"]'

#sql maps MongoDB syntax
CON_MAP = {
    '=':'$eq',
    '<':'$lt',
    '<=':'$lte',
    '>':'$gt',
    '>=':'$gte',
    '!=':'$ne',
}