#coding:utf-8

"""
	author	: linkin
	date	: 2019.03.02
	email	: yooleak@outlook.com

"""
import re
import hashlib

def from_pattern(content,pattern,index=0,allget=False):
	finds = re.findall(pattern,content)
	if finds:
		if allget:
			return finds
		else:
			return finds[index]
	
def md5(string):
	hashed = hashlib.md5()
	hashed.update(string.encode('utf-8'))
	md5ed = hashed.hexdigest()
	return md5ed
