#-*- coding: UTF-8 -*- 
from flask import Blueprint
from flask import request,jsonify,json
from models import *
import os, stat
from PIL import Image, ExifTags, ImageOps
import string
import shutil
import uuid

uploadImage_route = Blueprint('upload_image', __name__)

@uploadImage_route.route("/uploadpicture", methods=['POST'])
def uploadavatar():
	try:
		print "avatar"
		jsonstring = request.form.get('json')
		jsonstring = json.loads(jsonstring)
		token = jsonstring['token']
		type = jsonstring['type'] 
		number = jsonstring.get('number','')
		usertype = jsonstring.get('usertype','')
		src = request.form.get('avatar_path')
		u = getuserinformation(token)
		id = u.id
		try:
			state = 'successful'
			reason = ''
			if type=="0":
				avatartmp = getavatarvoicebyuserid(id)
				if avatartmp!=None:
					avatarnumber = avatartmp.avatar_number if avatartmp.avatar_number != None else 0
					avatarnumber = avatarnumber + 1
					#路径
					dst = '/home/www/avatar/' + str(id) + '-' + str(avatarnumber)
					avatarurl = "http://218.244.147.240:80/avatar/" + str(id) + '-' + str(avatarnumber)
					#更新数据库
					avatartmp.avatar_number = avatarnumber
					avatartmp.avatarurl = avatarurl
					avatartmp.gender = u.gender
					avatartmp.name = u.name
					avatartmp.disable = 0
					avatartmp.add()
				else:
					avatarnumber = 1
					#路径
					dst = '/home/www/avatar/' + str(id) + '-' + str(avatarnumber)
					avatarurl = "http://218.244.147.240:80/avatar/" + str(id) + '-' + str(avatarnumber)
					#第一次上传头像，新增
					tmp = avatarvoice(userid = id,avatarurl = avatarurl,avatar_number = avatarnumber,gender = u.gender,name = u.name)
					tmp.add()
				#移动文件
				shutil.copy(src, dst)
				os.chmod(dst, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP  | stat.S_IROTH)
				#生成卡片头像
				fp = Image.open(dst)
				fp.thumbnail((500,500))
				fp.save(dst + '_card.jpg')
				#生成缩略图
				fp = Image.open(dst)
				fp.thumbnail((200,200))
				fp.save(dst + '_thumbnail.jpg')
				#为了兼容性加的东西
				dst = '/home/www/avatar/' + str(id)
			elif type == "10":
				#type = 10 表示食光
				dst = '/home/www/static/shiguang/avatar/' + str(number)
			elif type == "11":
				#type = 11 表示食光
				dst = '/home/www/static/shiguang/cusAvatar/' + str(number)
			elif type == "12":
				#type = 12 表示食光
				dst = '/home/www/static/shiguang/foodimg/' + str(number)
			elif type == "13":
				#type = 13 表示食光
				dst = '/home/www/static/shiguang/homeimg/' + str(number)
			elif type == "14":
				#type = 14 表示食光
				dst = '/home/www/static/shiguang/top/' + str(number)
			else:
				state = 'fail'
				reason = 'no this type'				
				dst = '/home/www/picture/temp/' + str(id)
			'''
			if os.path.exists(dst):
				os.remove(dst)
				os.remove(dst + '_thumbnail.jpg')
			'''

			shutil.move(src, dst)
			os.chmod(dst, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP  | stat.S_IROTH)
			if type =="0":
				fp = Image.open(dst)
				# fp.thumbnail((200,200))
				fp = thumnail_enhanced(fp, 200, 200)
				if fp:
					fp.save(dst + '_thumbnail.jpg')
			if type == "10" or type == "11":
				fp = Image.open(dst)
				# fp.thumbnail((200,200))
				fp = thumnail_enhanced(fp, 200, 200)
				if fp:
					fp.save(dst + '_thumbnail.jpg')

		except Exception, e:
			print e 
			state = 'fail'
			reason = '上传图片失败,请重传'
	except Exception, e:
		print e 
		id=''
		state = 'fail'
		reason= '异常,请重传'


	response = jsonify({'id':id,
						'state':state,
						'reason':reason})
	return response

