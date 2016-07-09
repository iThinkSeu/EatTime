#-*- coding: UTF-8 -*- 
from flask import Blueprint
from flask import request,jsonify,json
import traceback
import sys
sys.path.append("..")
from models import *
from functions.hashmd5 import *
from functions.sendMsg import *


orderList_route = Blueprint('orderList', __name__)

@orderList_route.route("/orderuser",methods=['POST'])
def orderuser():
	try:
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