#-*- coding: UTF-8 -*-
import sys
sys.path.append("..")
from flask import Blueprint
from flask import request,jsonify,json
from models import *
import os, stat
from PIL import Image, ExifTags, ImageOps
import string
import shutil
import uuid

uploadImage_route = Blueprint('upload_image', __name__)

def thumnail_enhanced(image, width, height):
	try:
		if hasattr(image, '_getexif'):
			for orientation in ExifTags.TAGS.keys():
				if ExifTags.TAGS[orientation] == 'Orientation':
					break
			e = image._getexif()
			if e is not None:
				exif = dict(e.items())
				orientation = exif.get(orientation, None)
				if orientation is None: return

				if orientation == 3: image = image.transpose(Image.ROTATE_180)
				elif orientation == 6: image = image.transpose(Image.ROTATE_270)
				elif orientation == 8: image = image.transpose(Image.ROTATE_90)

		# image.thumbnail((width, height), Image.ANTIALIAS)
		# background = Image.new('RGBA', (width, height), (255, 255, 255, 0))
		# background.paste(image,((width - image.size[0]) / 2, (height - image.size[1]) / 2))
		return ImageOps.fit(image, (width, height), Image.ANTIALIAS)

	except:
		return


@uploadImage_route.route("/uploadpicture", methods=['POST'])
def uploadavatar():
	try:
		print "avatar"
		jsonstring = request.form.get('json')
		jsonstring = json.loads(jsonstring)
		token = jsonstring['token']
		type = jsonstring.get('type','')
		print type+"test"
		number = jsonstring.get('number','')
		usertype = jsonstring.get('usertype','')
		src = request.form.get('avatar_path')
		u = getuserinformation(token)
		id = ''
		print type
		print "avatar2"
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
				dst = '/home/www/avatar/' + str(number)
			elif type == "10":
				#type = 10 表示商家头像
				url = 'http://119.29.233.72:3001/uploadfiles/shiguang/avatar/' + 'avatar'+str(number)
				u = User.query.filter_by(id=number).first()
				if u!=None:
					u.headimgurl = url
					u.addchange()
				else:
					return jsonify({'id':'',
									'state':'fail',
									'reason':'no this id'})
				dst = '/home/www/uploadfiles/shiguang/avatar/' + 'avatar'+str(number)
			elif type == "11":
				#type = 11 表示客户头像
				dst = '/home/www/uploadfiles/shiguang/cusAvatar/' + 'cusAvatar'+str(number)
			elif type == "12":
				#type = 12 表示食物图片
				db.session.commit()
				imageurl = "http://119.29.233.72:3001/uploadfiles/shiguang/foodimg/" + 'food'+str(number)+'.jpg'
				img = food.query.filter_by(id=number).first()
				if img!=None:
					img.addimage(imageurl)
				else:
					return jsonify({'id':'',
									'state':'fail',
									'reason':'no this food'})
				dst = '/home/www/uploadfiles/shiguang/foodimg/'  + 'food'+str(number)+'.jpg'
			elif type == "13":
				#type = 13 表示主页图片
				url = 'http://119.29.233.72:3001/uploadfiles/shiguang/homeimg/' + 'homeimg'+str(number)+'.jpg'
				u = User.query.filter_by(id=number).first()
				if u!=None:
					u.homeimgurl = url
					u.addchange()
				else:
					return jsonify({'id':'',
									'state':'fail',
									'reason':'no this id'})
				dst = '/home/www/uploadfiles/shiguang/homeimg/' + 'homeimg'+str(number)+'.jpg'
			elif type == "14":
				#type = 14 表示滑动图片
				dst = '/home/www/uploadfiles/shiguang/top/' + 'top'+str(number)+'.jpg'
			elif type == "15":
				#type = -1 表示confirm image
				url = 'http://119.29.233.72:3001/uploadfiles/shiguang/confirm/' +str(number)+'.jpg'
				if u!=None:
					if number==1:
						u.cookLifeimgurl = url
					elif number ==2:
						u.cookEnvirimgurl = url
					else:
						u.bestFoodimgurl = url
					u.addchange()
				else:
					return jsonify({'id':'',
									'state':'fail',
									'reason':'no this id'})
				dst = '/home/www/uploadfiles/shiguang/confirm/' +str(number)+'.jpg'
			else:
				state = 'fail'
				reason = 'no this type'
				dst = '/home/www/uploadfiles/temp/' +str(number)+'.jpg'
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
			if type == "10" or type == "11" or type=="12" or type=="13" or type=="14" or type=="15":
				fp = Image.open(dst)
				# fp.thumbnail((200,200))
				fp = thumnail_enhanced(fp, 400, 400)
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

