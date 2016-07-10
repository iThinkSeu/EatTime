#-*- coding: UTF-8 -*-
from flask import Blueprint
from flask import request,jsonify,json
import traceback
import sys
sys.path.append("..")
from models import *
from functions.hashmd5 import *
from functions.sendMsg import *
from functions.DBFunctions import *


commitOrderList_route = Blueprint('commitOrderList', __name__)

@commitOrderList.route("/commitOrderList",methods=['POST'])
def commitOrderList():
	try:
		token = request.json['token']
		sellerId = request.json.get('sellerId','')
		foodList = request.json.get('foodList',[])
		peoplenumber = request.json.get('peopleNumer', 1)
		#price = request.json['price']
		customerUser = get_customer_user_by_token(token)
		seller = get_user_by_id(userid)
		if customerUser is None:
			olderListid = ''
			state = 'fail'
			reason = 'unvalid customer user'
			repsone = jsonify({'orderListid':olderListid, 'state':state, 'reason':reason})
			return response

		if seller is None:
			olderListid = ''
			state = 'fail'
			reason = 'unvalid seller user'
			repsone = jsonify({'orderListid':olderListid, 'state':state, 'reason':reason})
			return response

		price = 0;
		for foodid in foodList:
				food = get_food_by_id(foodid)
				if food is None:
					olderListid = ''
					state = 'fail'
					reason = 'unvalid food: ' + str(foodid)
					repsone = jsonify({'olderListid':orderListid, 'state':state, 'reason':reason})
					return response
				price += food.price

		flag, orderListTemp = customerUser.orderuser(seller, peoplenumber, price, 0)

		if flag == 0:
			for foodid in foodList:
				food = get_food_by_id(foodid)
				if orderListTemp.addfood(food) == 2:
					olderListid = ''
					state = 'fail'
					reason = 'database error@2'
					repsone = jsonify({'olderListid':orderListid, 'state':state, 'reason':reason})
					return response
			olderListid = ''
			state = 'successful'
			reason = ''
			response = jsonify({'state':state,
			                  'reason':reason})
			return response
		else :
			state = 'fail'
			reason = 'database error@1'
			response = jsonify({'state':state,
			                  'reason':reason})
			return response
	except Exception, e:
