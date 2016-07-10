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
from datetime import *


commitOrderList_route = Blueprint('commitOrderList', __name__)

@commitOrderList_route.route("/commitOrderList",methods=['POST'])
def commitOrderList():
	try:
		token = request.json['token']
		sellerId = request.json.get('sellerId','')
		foodList = request.json.get('foodList',[])
		peoplenumber = request.json.get('peopleNumer', 1)
		#price = request.json['price']
		eatTime = request.json['planEatTime']
		customerUser = get_customer_user_by_token(token)
		seller = get_user_by_id(sellerId)
		if customerUser is None:
			orderedTime = ''
			planEatTime = ''
			olderListid = ''
			state = 'fail'
			reason = 'unvalid customer user'
			response = jsonify({'orderListid':olderListid, 'state':state, 'reason':reason, 'orderedTime':orderedTime, 'planEatTime':planEatTime})
			return response

		if seller is None:
			orderedTime = ''
			planEatTime = ''
			olderListid = ''
			state = 'fail'
			reason = 'unvalid seller user'
			response = jsonify({'orderListid':olderListid, 'state':state, 'reason':reason, 'orderedTime':orderedTime, 'planEatTime':planEatTime})
			return response

		price = 0;
		for foodid in foodList:
				food = get_food_by_id(foodid)
				if food is None:
					orderedTime = ''
					planEatTime = ''
					olderListid = ''
					state = 'fail'
					reason = 'unvalid food: ' + str(foodid)
					response = jsonify({'orderListid':olderListid, 'state':state, 'reason':reason, 'orderedTime':orderedTime, 'planEatTime':planEatTime})
					return response
				price += food.price

		flag, orderListTemp = customerUser.orderuser(seller, peoplenumber, price, 0)

		orderListTemp.token = generatemd5(str(orderListTemp.id))
		orderListTemp.add()



		if flag == 0:
			for foodid in foodList:
				food = get_food_by_id(foodid)
				if orderListTemp.addfood(food) != 0:
					orderedTime = ''
					planEatTime = ''
					olderListid = ''
					state = 'fail'
					reason = 'database error@food'
					response = jsonify({'orderListid':olderListid, 'state':state, 'reason':reason, 'orderedTime':orderedTime, 'planEatTime':planEatTime})
					return response
			orderedTime = orderListTemp.ordertime
			minutes = timedelta(minutes=eatTime)
			planEatTime = orderedTime + minutes
			orderListTemp.planeattime = planEatTime
			orderListTemp.add()
			olderListid = orderListTemp.token
			state = 'successful'
			reason = ''
			response = jsonify({'orderListid':olderListid, 'state':state, 'reason':reason, 'orderedTime':orderedTime, 'planEatTime':planEatTime})
			return response
		else :
			orderedTime = ''
			planEatTime = ''
			olderListid = ''
			state = 'fail'
			reason = 'database error@orderList'
			response = jsonify({'orderListid':olderListid, 'state':state, 'reason':reason, 'orderedTime':orderedTime, 'planEatTime':planEatTime})
			return response
	except Exception, e:
		print e
		orderedTime = ''
		planEatTime = ''
		olderListid = ''
		state = 'fail'
		reason = 'exception'
		response = jsonify({'orderListid':olderListid, 'state':state, 'reason':reason, 'orderedTime':orderedTime, 'planEatTime':planEatTime})
		return response
