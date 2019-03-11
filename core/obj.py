#coding:utf-8

"""
	author	: linkin
	date	: 2019.03.04
	email	: yooleak@outlook.com

"""
import os
import w3lib.url
from PIL import Image
from config import WIDTH,HEIGHT
from settings import IMAGE_RATIO
from util.http import send_request
from decorator import force_type
from core.log import getLogger

logger = getLogger(__name__)

class BinaryImage:

	@force_type({1:str})
	def __init__(self,path_or_url):
		self.string = path_or_url

	def to_binary(self):
		if os.path.isfile(self.string):
			with open(self.string,'rb') as f:
				pic = f.read()
		elif w3lib.url.is_url(self.string):
				response = send_request(self.string)
				pic = response.content
		else:
			raise TypeError(f'Expected a url or disk path,got "{self.string}".')
		return pic


class ImageHandler:

    def __init__(self, path_or_url, aspect_width=WIDTH, aspect_height=HEIGHT,temp_name='temp.jpg'):
        self.string = path_or_url
        self.aspect_width = aspect_width
        self.aspect_height = aspect_height
        self.temp_name = temp_name
        self.result_image = None
        self._img = None
        self.finnal_path= None

    @property
    def img(self):
    	if self._img:
    		return self._img
    	if os.path.isfile(self.string):
    		self._img = Image.open(self.string)
    		self.finnal_path=self.string
    		return self._img
    	elif w3lib.url.is_url(self.string):	
    		self.download_image(self.string,self.temp_name)
    		self._img =  Image.open(self.temp_name)
    		self.finnal_path = self.temp_name
    		return self._img
    	else:
    		raise TypeError(f'Expected a url or disk path,got "{self.string}".')
    
    def download_image(self,url,path=None):
    	with open(path,'wb') as f:
    		response = send_request(url)
    		f.write(response.content)

    def ratio_or_resize(self):
        img_width = self.img.size[0]
        img_height = self.img.size[1]
        ratio = img_height / img_width
        logger.info(f'The image "{self.string}" height/width ratio is {ratio}.')
        if IMAGE_RATIO[0] <= ratio <= IMAGE_RATIO[1]:
        	return 
        else:
        	logger.info(f'The image isn\'t not in a allowed aspect ratio,resizing into width:{self.aspect_width},height:{self.aspect_height}')
	        if (img_width / img_height) > (self.aspect_width / self.aspect_height):
	            rate = self.aspect_width / img_width
	        else:
	            rate = self.aspect_height / img_height
        rate = round(rate, 1)
        self._img = self.img.resize((int(img_width * rate), int(img_height * rate)))
        return self
 
    def past_background(self):
        self.result_image = Image.new("RGB", [self.aspect_width, self.aspect_height], (255, 255, 255, 255))
        self.result_image.paste(self.img, (int((self.aspect_width - self.img.size[0]) / 2), int((self.aspect_height - self.img.size[1]) / 2)))
        return self
 
    def save_result(self, file_name):
        self.result_image.save(file_name)

    def to_valid_post_image_path(self):
    	if self.ratio_or_resize() is None:
    		return self.finnal_path
    	else:
    		self.past_background().save_result(self.temp_name)
    		return self.temp_name

 
 
if __name__ == "__main__":
    ImageHandler(r"https://images.unsplash.com/photo-1519058082700-08a0b56da9b4?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1000&q=80").ratio_or_resize().past_background().save_result("temp.jpg")
 

	


