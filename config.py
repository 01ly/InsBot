#coding:utf-8

"""
	author	: linkin
	date	: 2019.03.02
	email	: yooleak@outlook.com

"""
USERNAME = ''
PASSWORD = ''
#the default resized width and height of a user posting image 
#while the image isn't in a allowed aspect ratio
WIDTH,HEIGHT = 1500,1500
# time delays between requests.
DELAY = 2
# requests failed retry times.
REQUEST_FAIL_RETRY = 3
# global proxy.
# If depends on your computer proxy port.
IP_PORT  = '127.0.0.1:1087'
PROXY_GLOBAL = {
    'https' :f'https://{IP_PORT}',
    'http'  :f'http://{IP_PORT}',
}
# MongoDB settings.
MONGODB = {
    'host'          :'127.0.0.1',
    'port'          :27017,
    'user'          : '',
    'password'      : '',
    'database'      :'Instagram',
    'fans'          :'Followers',
    'following'     :'Followings',
    'channel'       :'ChannelPosts',
    'tagged'        :'TaggedPosts',
    'comments'      :'Comments',
    'under_tag'     :'UnderTagPosts',
    'media_liker'   :'MediaLiker',
    'comment_liker' :'CommentLiker',
}
# the max amount of crawling user's posts.
USER_POSTS_MAX  = 100 
#logging settings.
#enable logging.
LOG_ENABLE = True
#logging level.
LOG_LEVEL = 'INFO'
#logging file encoding.
LOG_FILE_ENCODING = 'UTF-8'
#logging file save path.
LOG_FILE_SAVE_PATH = r'txt/log.txt'
#logging file time format.
LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
#corresponding logging format to each logging level.
LOG_FORMAT = {
    'DEBUG'     : '%(asctime)s %(name)s(%(levelname)s) - %(message)s',
    'INFO'      : '%(asctime)s %(name)s(%(levelname)s) - %(message)s',
    'WARNING'   : '%(asctime)s %(name)s(%(levelname)s) - %(message)s',
    'ERROR'     : '%(asctime)s %(name)s(%(levelname)s) - %(message)s',
    'CRITICAL'  : '%(asctime)s %(name)s(%(levelname)s) - %(message)s',
}