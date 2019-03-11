#coding:utf-8

"""
	author	: linkin
	date	: 2019.03.02
	email	: yooleak@outlook.com

"""
import random

def get_location_params(ins_obj,json_res,location=None,fuzzy=False):
	locations = json_res['venues']
	status = json_res['status']
	if status == 'ok' and locations:
		for i in locations:
			if not fuzzy:
				if i['name']==location:
					return {"lat":i["lat"],"lng":i["lng"],"facebook_places_id":i["external_id"]}
			else:
				if i['name'].startswith(location):
					return {"lat":i["lat"],"lng":i["lng"],"facebook_places_id":i['external_id']}


def inner_photo_tagged_pos(userIds):
	inners = []
	for i in userIds:
		_ = {"user_id":f'{i}',"position":[random.randrange(1,10**16)/10**16,
		random.randrange(1,10**16)/10**16]}
		inners.append(_)
	return {"in":inners}


