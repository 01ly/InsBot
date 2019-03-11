#coding:utf-8

"""
	author	: linkin
	date	: 2019.03.02
	email	: yooleak@outlook.com

"""

def login_required(func):
	def wrapper(self,*args,**kwargs):
		if not self.logined:
			self.login()
		return func(self,*args,**kwargs)
	return wrapper

def force_type(index_type_dict):
	def outter(func):
		def wrappers(self,*args,**kwargs):
			if not isinstance(index_type_dict,dict):
				raise TypeError(f'Expected a dict,got "{type(index_type_dict).__name__}".')
			for index,_type in index_type_dict.items():
				if isinstance(index,int):
					if not isinstance(args[index-1],_type):
						raise TypeError(f'Wrong param type for method "{func.__name__}" which index is {index}.'
							f'Expected "{_type.__name__}",got "{type(args[index-1]).__name__}".')
				elif isinstance(index,str):
					try:
						if not isinstance(kwargs[index],_type):
							raise TypeError(f'Wrong param type for method "{func.__name__}" which key is "{index}".'
								f'Expected "{_type.__name__}",got "{type(kwargs[index]).__name__}".')
					except KeyError:
						continue
			return func(self,*args,**kwargs)
		return wrappers
	return outter

				 




