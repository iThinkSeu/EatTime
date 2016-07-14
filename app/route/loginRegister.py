#-*- coding: UTF-8 -*-
from flask import Blueprint
from flask import request,jsonify,json
import traceback
import sys
sys.path.append("..")
from models import *
from functions.hashmd5 import *
from functions.sendMsg import *
import random


loginRegister_route = Blueprint('loginRegister', __name__)


@loginRegister_route.route('/sendsmscode', methods=['POST'])
def send_sms_code():
	try:
		db.session.commit()
		phone = request.json['phone']
		type_flag = request.json['type']
		u = User.query.filter_by(username=phone).first()
		if u or str(type_flag) == '1':
			state = 'successful'
			reason = ''
			code = str(random.randint(100000, 999999))
			if str(type_flag) == '1' or str(type_flag) == '2':
				rv = send_sms_code_by_type(str(phone), code, str(type_flag))
				if rv != 0:
					state = 'fail'
					reason = '验证码发送失败'
				else:
					p = checkMsg.query.filter_by(phone = str(phone)).first()
					if p is None:
						sms_code = checkMsg(phone=str(phone), code=code)
						sms_code.add()
					else:
						p.code = code
						p.timestamp = datetime.now()
						p.add()
			else:
				state = 'fail'
				reason = 'invalid'
		else:
			state = 'fail'
			reason = '该手机号尚未注册'
	except Exception, e:
		print e
		state = 'fail'
		reason = '服务器异常'

	print state, reason
	return jsonify({'state':state, 'reason':reason})

@loginRegister_route.route('/registerphone', methods=['POST'])
def register_user():
	try:
		db.session.commit()
		id = ''
		token = ''
		phone = request.json['phone']
		password = request.json['password']
		code = request.json['code']
		u = User.query.filter_by(username = str(phone)).first()
		if u is None:
			p = checkMsg.query.filter_by(phone=str(phone)).first()
			if p is None:
				state = 'fail'
				reason = '验证码无效'
			else:
				state = 'successful'
				reason = ''
				token = hashToken(str(phone), password+str(code))
				u = User(username = phone, password = password, token = token)
				u.add()
				id = getuserinformation(token).id
		else:
			state  = 'fail'
			reason = '该手机号已被注册'
	except Exception, e:
		print e
		state = 'fail'
		reason = '服务器异常'

	return jsonify({'state':state, 'reason':reason, 'token':token, 'id':id})


@loginRegister_route.route('/sendsmscodecus', methods=['POST'])
def sendsmscodecus():
	try:
		db.session.commit()
		phone = request.json['phone']
		type_flag = request.json['type']
		u = customerUser.query.filter_by(username=phone).first()
		if u or str(type_flag) == '1':
			state = 'successful'
			reason = ''
			code = str(random.randint(100000, 999999))
			if str(type_flag) == '1' or str(type_flag) == '2':
				rv = send_sms_code_by_type(str(phone), code, str(type_flag))
				if rv != 0:
					state = 'fail'
					reason = '验证码发送失败'
				else:
					p = checkMsg.query.filter_by(phone = str(phone)).first()
					if p is None:
						sms_code = checkMsg(phone=str(phone), code=code)
						sms_code.add()
					else:
						p.code = code
						p.timestamp = datetime.now()
						p.add()
			else:
				state = 'fail'
				reason = 'invalid'
		else:
			state = 'fail'
			reason = '该手机号尚未注册'
	except Exception, e:
		print e
		state = 'fail'
		reason = '服务器异常'

	print state, reason
	return jsonify({'state':state, 'reason':reason})

@loginRegister_route.route('/registerphonecus', methods=['POST'])
def registerphonecus():
	try:
		db.session.commit()
		id = ''
		token = ''
		phone = request.json['phone']
		password = request.json['password']
		code = request.json['code']
		u = customerUser.query.filter_by(username = str(phone)).first()
		if u is None:
			p = checkMsg.query.filter_by(phone=str(phone)).order_by(checkMsg.timestamp.desc()).first()
			if p is None or p.code != str(code) or (datetime.now()-p.timestamp > timedelta(minutes=5)):
				state = 'fail'
				reason = '验证码无效'
			else:
				state = 'successful'
				reason = ''
				token = hashToken(str(phone), password+str(code))
				u = User(username = phone, password = password, token = token)
				u.add()
				id = getuserinformation(token).id


		else:
			state  = 'fail'
			reason = '该手机号已被注册'
	except Exception, e:
		print e
		state = 'fail'
		reason = '服务器异常'

	return jsonify({'state':state, 'reason':reason, 'token':token, 'id':id})


@loginRegister_route.route('/resetpassword', methods=['POST'])
def reset_password():
	try:
		db.session.commit()
		id = ''
		token = ''
		phone = request.json['phone']
		password = request.json['password']
		code = request.json['code']
		u = User.query.filter_by(username = str(phone)).first()
		if u is not None:
			p = checkMsg.query.filter_by(phone=str(phone)).first()
			if p is None or p.code != str(code) or (datetime.now()-p.timestamp > timedelta(minutes=5)):
				state = 'fail'
				reason = '验证码无效'
			else:
				state = 'successful'
				reason = ''
				token = hashToken(str(phone), password+str(code))
				u.password = password
				u.token = token
				id = u.id
				try:
					db.session.add(u)
					db.session.commit()
				except Exception, e:
					print e
					db.session.rollback()

		else:
			state  = 'fail'
			reason = '该手机号尚未被注册'

	except Exception, e:
		print e
		state = 'fail'
		reason = '服务器异常'
	return jsonify({'state':state, 'reason':reason, 'token':token, 'id':id})




@loginRegister_route.route("/register",methods=['POST'])
def register():
	try:
		"""
		username=request.json[u'username']
		password=request.json['password']
		temp = checkName(username)
		if temp==False:
			response = jsonify({
								'id':'',
								'state':'fail',
								'reason':'用户名不能包含中文且至少要两个字母',
								'token':'chinese'})
			return response
		token= hashToken(username,password)
		u=User(username=username,password=password,token=token)
		if u.isExistedusername() == 0:
			##未完成，加code验证码判断相关逻辑
			u.add()
			state = 'successful'
			reason = ''
			token = hashToken(username,password)
			id = getuserinformation(token).id
		else:
			state = 'fail'
			reason = '用户名已被注册'
			token = 'Haveresiger'
			id=''
		"""
		state = "fail"
		reason = "旧版已废弃，请升级至最新版本（weme.space可下载）"
		id = ''
		token = ''
	except Exception, e:
		print e
		state = 'fail'
		reason ='异常'
		token = 'exception'
		id=''

	response = jsonify({
						'id':id,
						'state':state,
						'reason':reason,
						'token':token})
	return response


@loginRegister_route.route("/login",methods=['POST'])
def login():
	try:
		username = request.json['username']
		password = request.json['password']
		u=User(username=username,password=password)
		gender = ''
		if u.isExisted():
			state = 'successful'
			tmp = getTokeninformation(username)
			token = tmp.token
			gender = tmp.gender
			id = tmp.id
			reason = ''
		else:
			tempuser = User.query.filter_by(username=username).first()
			if tempuser != None:
				pwd = generatemd5(tempuser.password)
				if pwd == password:
					state = 'successful'
					token = tempuser.token
					reason = ''
					id = tempuser.id
					tempuser.password = pwd
					tempuser.addpwd()
					gender = tempuser.gender
				else:
					id=''
					state = 'fail'
					token = 'None'
					reason = '用户名密码错误'
			else:
				id=''
				state = 'fail'
				token = 'None'
				reason = '用户名密码错误'
	except Exception, e:
		print "login error!!"
		print e
		state = 'fail'
		reason='服务器异常'
		token = 'None'
		id = ''

	response = jsonify({'id':id,
						'gender':gender,
						'state':state,
						'reason':reason,
						'token':token})
	#print state, reason
	return response

@loginRegister_route.route("/appregister",methods=['POST'])
def appregister():
	try:
		db.session.commit()
		username = request.json.get('username','')
		password = request.json.get('password','')
		token = ''
		id = ''
		token= hashToken(username,password)
		u=User(username=username,password=password,token=token)
		if u.isExistedusername() == 0:
			##未完成，加code验证码判断相关逻辑
			u.add()
			state = 'successful'
			reason = ''
			token = hashToken(username,password)
			id = getuserinformation(token).id
		else:
			state = 'fail'
			reason = '用户名已被注册'
			token = 'Haveresiger'
			id=''

	except Exception, e:
		print e
		state = 'fail'
		reason = 'exception'

	response = jsonify({'state':state,'reason':reason,'token':token,'id':id})
	return response

@loginRegister_route.route("/applogin",methods=['POST'])
def applogin():
	try:
		db.session.commit()
		username = request.json['username']
		password = request.json['password']
		u=User(username=username,password=password)
		if u.isExisted():
			state = 'successful'
			tmp = getTokeninformation(username)
			token = tmp.token
			id = tmp.id
			reason = ''
		else:
			id=''
			state = 'fail'
			token = 'None'
			reason = '用户名密码错误'
	except Exception, e:
		print "login error!!"
		print e
		username = ''
		password = ''
		state = 'fail'
		reason='服务器异常'
		token = 'None'
		id = ''

	response = jsonify({'id':id,
						'state':state,
						'username':username,
						'reason':reason,
						'token':token})
	#print state, reason
	return response


@loginRegister_route.route("/cuslogin",methods=['POST'])
def cuslogin():
	try:
		db.session.commit()
		username = request.json['username']
		password = request.json['password']
		u=customerUser(username=username,password=password)
		if u is not None:
			state = 'successful'
			tmp = getTokeninformation(username)
			token = tmp.token
			id = tmp.id
			reason = ''
		else:
			id=''
			state = 'fail'
			token = 'None'
			reason = '用户名密码错误'
	except Exception, e:
		print "login error!!"
		print e
		username = ''
		password = ''
		state = 'fail'
		reason='服务器异常'
		token = 'None'
		id = ''

	response = jsonify({'id':id,
						'state':state,
						'username':username,
						'reason':reason,
						'token':token})
	#print state, reason
	return response
