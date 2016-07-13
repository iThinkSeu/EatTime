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


orderList_route = Blueprint('orderList', __name__)

@orderList_route.route("/commitOrderList",methods=['POST'])
def commitOrderList():
	try:
		token = request.json['token']
		sellerId = request.json.get('sellerId','')
		foodList = eval(request.json.get('foodList',''))
		peoplenumber = request.json.get('peopleNumer', 1)
		#price = request.json['price']
		eatTime = request.json['planEatTime']
		customerUser = get_customer_user_by_token(token)
		seller = get_user_by_token(sellerId)
		if customerUser is None:
			orderedTime = ''
			planEatTime = ''
			olderListid = ''
			state = 'fail'
			reason = '无效的用户'
			response = jsonify({'orderListid':olderListid, 'state':state, 'reason':reason, 'orderedTime':orderedTime, 'planEatTime':planEatTime})
			return response

		if seller is None:
			orderedTime = ''
			planEatTime = ''
			olderListid = ''
			state = 'fail'
			reason = '被不存在该商家'
			response = jsonify({'orderListid':olderListid, 'state':state, 'reason':reason, 'orderedTime':orderedTime, 'planEatTime':planEatTime})
			return response

		price = 0;
		for foodid, number in foodList:
				food = get_food_by_id(foodid)
				if food is None:
					orderedTime = ''
					planEatTime = ''
					olderListid = ''
					state = 'fail'
					reason = '无效的食物，食物编号： ' + str(foodid)
					response = jsonify({'orderListid':olderListid, 'state':state, 'reason':reason, 'orderedTime':orderedTime, 'planEatTime':planEatTime})
					return response
				price += (food.price * number)

		flag, orderListTemp = customerUser.orderuser(seller, peoplenumber, price, 0)

		orderListTemp.token = generatemd5(str(orderListTemp.id))
		orderListTemp.add()



		if flag == 0:
			for foodid, number in foodList:
				food = get_food_by_id(foodid)
				if orderListTemp.addfood(food, number) != 0:
					orderedTime = ''
					planEatTime = ''
					olderListid = ''
					state = 'fail'
					reason = '食物数据库异常'
					response = jsonify({'orderListid':olderListid, 'state':state, 'reason':reason, 'orderedTime':orderedTime, 'planEatTime':planEatTime})
					return response
			orderedTime = orderListTemp.ordertime
			#minutes = timedelta(minutes=eatTime)
			planEatTime = datetime.strptime(eatTime, "%Y-%m-%d %H:%M:%S")
			orderListTemp.planeattime = planEatTime
			orderListTemp.add()
			olderListid = orderListTemp.token
			state = 'successful'
			reason = '已成功下单'
			response = jsonify({'orderListid':olderListid, 'state':state, 'reason':reason, 'orderedTime':orderedTime.strftime("%Y-%m-%d %H:%M:%S"), 'planEatTime':planEatTime.strftime("%Y-%m-%d %H:%M:%S")})
			return response
		else :
			orderedTime = ''
			planEatTime = ''
			olderListid = ''
			state = 'fail'
			reason = '订单数据库异常'
			response = jsonify({'orderListid':olderListid, 'state':state, 'reason':reason, 'orderedTime':orderedTime, 'planEatTime':planEatTime})
			return response

	except Exception, e:
		print e
		orderedTime = ''
		planEatTime = ''
		olderListid = ''
		state = 'fail'
		reason = '服务器异常'
		response = jsonify({'orderListid':olderListid, 'state':state, 'reason':reason, 'orderedTime':orderedTime, 'planEatTime':planEatTime})
		return response


@orderList_route.route('/sellerConfirmOrder', methods = ['POST'])
def sellerConfirmOrder():
	try:
		sellerToken = request.json['token']
		orderId = request.json['orderId']

		seller = get_user_by_token(sellerToken)
		if seller is not None:
			order = seller.beordered.filter_by(token = orderId).first()
			if order is not None:
				if order.paystate == 0:
					state = 'successful'
					reason = '该订单已经确认'
					order.paystate = 1
					db.session.commit()
			else :
				state = 'fail'
				reason = '无效的订单'
		else :
			state = 'fail'
			reason = '无效的用户'
	except Exception, e:
		print e
		state = 'fail'
		reason = '服务器异常'

	response = jsonify({
	                   "state":state,
	                   "reason":reason
	                   })
	return response


@orderList_route.route("/sellerCancelOrder", methods = ['POST'])
def sellerCancelOrder():
	try:
		sellerToken = request.json['token']
		orderId = request.json['orderId']
		seller = get_user_by_token(sellerToken)
		if seller is not None:
			order = seller.beordered.filter_by(token = orderId).first()
			if order is not None:
				if order.paystate == 0:
					order.paystate = 3
					order.add()
					state = 'successful'
					reason = '订单取消成功'
				elif order.paystate == 1 or order.paystate == 7:
					order.paystate = 5
					order.add()
					state = 'successful'
					reason = '订单取消成功'
				elif order.paystate == 2:
					state = 'fail'
					reason = '不能取消已经完成的订单'
				else :
					state = 'fail'
					reason = '该订单已经被取消'
			else :
				state = 'fail'
				reason = '无效的订单'
		else :
			state = 'fail'
			reason = '无效的用户'
	except Exception, e:
		print e
		state = 'fail'
		reason = '服务器异常'

	response = jsonify({'state':state,
	                   'reason':reason})
	return response

@orderList_route.route("/customerCancelOrder", methods = ['POST'])
def customerCancelOrder():
	try:
		customerToken = request.json['token']
		orderId = request.json['orderId']
		customer = get_customer_user_by_token(customerToken)
		if customer is not None:
			order = customer.order.filter_by(token = orderId).first()
			if order is not None:
				if order.paystate == 0:
					order.paystate = 4
					order.add()
					state = 'successful'
					reason = '取消订单成功'
				elif order.paystate == 1 or order.paytstate == 7:
					state = 'fail'
					reason = '对不起，您现在无权取消订单'
				elif order.paystate == 2:
					state = 'fail'
					reason = '不能取消已经完成的订单'
				else :
					state = 'fail'
					reason = '该订单已经被取消'
			else :
				state = 'fail'
				reason = '无效的订单'
		else :
			state = 'fail'
			reason = '无效的用户'
	except Exception, e:
		print e
		state = 'fail'
		reason = '服务器异常'

	response = jsonify({'state':state,
	                   'reason':reason})
	return response


@orderList_route.route("/sellerOrder/<int:id>", methods = ['POST'])
def sellerOrder(id):
	try:
		sellerToken = request.json['token']
		page = int(request.json['page'])
		seller = get_user_by_token(sellerToken)
		if seller is not None:
			if id == 0:
				pageitems = seller.beordered.filter("paystate = 0").order_by(orderList.ordertime.desc()).paginate(page, per_page = 3, error_out = False)
			elif id == 1:
				pageitems = seller.beordered.filter(or_("paystate = 1" , "paystate = 7")).order_by(orderList.planeattime.desc()).paginate(page, per_page = 3, error_out = False)
			else:
				pageitems = seller.beordered.filter(or_("paystate = 2", "paystate = 6")).order_by(orderList.paytime.desc()).paginate(page, per_page = 3, error_out = False)
			headImg = ''
			availableOrderView = [{'orderId':item.token, 'planeEatTime':item.planeattime.strftime("%Y-%m-%d %H:%M:%S"), 'orderPrice':str(item.price), 'orderPayPrice':str(item.payprice) if item.payprice is not None else '', 'orderTime':item.ordertime.strftime("%Y-%m-%d %H:%M:%S"), 'orderPayTime':item.paytime.strftime("%Y-%m-%d %H:%M:%S") if item.paytime is not None else '', 'orderPeopleNumber':str(item.peoplenumber), 'customerId':str(item.orderuser.id), 'customerName':item.orderuser.username, 'customerHeadImg':headImg, 'customerHonesty':str(item.orderuser.honesty), 'customerFriendly':str(item.orderuser.friendly), 'customerPassion':str(item.orderuser.passion), 'foodName':','.join([foodi.foods.name for foodi in item.foodincludes]), 'foodCounts':str(sum([foodi.number for foodi in item.foodincludes]))} for item in pageitems.items]
			state = 'successful'
			reason = ''
			response = jsonify({'state':state,
			                   'reason':reason,
			                   'availableOrder':availableOrderView})
			return response
		else :
			state = 'fail'
			reason = '无效的用户'
			availableOrderView = []
			response = jsonify({'state':state,
			                   'reason':reason,
			                   'availableOrder':availableOrderView})
			return response
	except Exception, e:
		print e
		state = 'fail'
		reason = '服务器异常'
		availableOrderView = []
		response = jsonify({'state':state,
		                   'reason':reason,
		                   'availableOrder':availableOrderView})
		return response


@orderList_route.route("/customerOrder/<int:id>", methods = ['POST'])
def customerOrder(id):
	#try:
		customerToken = request.json['token']
		page = int(request.json['page'])
		customer = get_customer_user_by_token(customerToken)
		if customer is not None:
			if id == 0:
				pageitems = customer.order.filter("paystate = 0").order_by(orderList.ordertime.desc()).paginate(page, per_page = 3, error_out = False)
			elif id == 1:
				pageitems = customer.order.filter(or_("paystate = 1" , "paystate = 7")).order_by(orderList.planeattime.desc()).paginate(page, per_page = 3, error_out = False)
			else:
				pageitems = customer.order.filter(or_("paystate = 2", "paystate = 6")).order_by(orderList.paytime.desc()).paginate(page, per_page = 3, error_out = False)
			availableOrderView = [{'orderId':item.token, 'orderPlanEatTime':item.planeattime.strftime("%Y-%m-%d %H:%M:%S"), 'orderPrice':str(item.price), 'orderPayPrice':str(item.payprice) if item.payprice is not None else '', 'orderTime':item.ordertime.strftime("%Y-%m-%d %H:%M:%S"), 'orderPayTime':item.paytime.strftime("%Y-%m-%d %H:%M:%S") if item.paytime is not None else '', 'orderPeopleNumber':str(item.peoplenumber), 'sellerId':str(item.beordereduser.id), 'sellerName':item.beordereduser.username, 'sellerHeadImg':item.beordereduser.headimgurl, 'sellerScores':str(item.beordereduser.scoles), 'foodName':','.join([foodi.foods.name for foodi in item.foodincludes]), 'foodCounts':str(sum([foodi.number for foodi in item.foodincludes]))} for item in pageitems.items]
			state = 'successful'
			reason = ''
			response = jsonify({'state':state,
			                   'reason':reason,
			                   'availableOrder':availableOrderView})
			return response
		else :
			state = 'fail'
			reason = '无效的用户'
			availableOrderView = []
			response = jsonify({'state':state,
			                   'reason':reason,
			                   'availableOrder':availableOrderView})
			return response
	#except Exception, e:
	#	print e
	#	state = 'fail'
	#	reason = '服务器异常'
	#	availableOrderView = []
	#	response = jsonify({'state':state,
	#	                   'reason':reason,
	#	                   'availableOrder':availableOrderView})
	#	return response

@orderList_route.route('/sellerRequestPay', methods = ['POST'])
def sellerRequestPay():
	try :
		sellerToken = request.json['token']
		orderId = request.json['orderId']
		discount = request.json['discount']
		price = request.json['price']
		payprice = request.json['payprice']

		seller = get_user_by_token(sellerToken)
		if seller is not None:
			order = seller.beordered.filter_by(token = orderId).first()
			if order is not None:
				if order.paystate == 1:
					order.price = float(price)
					order.discount = float(discount)
					order.payprice = float(payprice)
					#order.paytime = datetime.now()
					order.paystate =  7
					customer = order.orderuser
					customer.friendly = 86
					customer.honesty = 90
					customer.passion = 90
					db.session.commit()
					#db.session.commit(customer)
					state = 'successful'
					reason = '请等待食客支付'
				elif order.paystate == 7:
					state = 'fail'
					reason = '别急~食客将会马上支付'
				else :
					state = 'fail'
					reason = '订单状态异常'
			else :
				state = 'fail'
				reason = '无效的订单'
		else :
			state = 'fail'
			reason = '无效的用户'
	except Exception, e:
		print e
		state = 'fail'
		reason = '服务器异常'

	response = jsonify({
	                   'state':state,
	                   'reason':reason
	                   })

	return response

@orderList_route.route('/customerConfirmPay', methods = ['POST'])
def customerConfirmPay():
	try:
		customerToken = request.json['token']
		orderId = request.json['orderId']
		orderScores = request.json.get('orderScores', '')

		customer = get_customer_user_by_token(customerToken)
		if customer is not None:
			order = customer.order.filter_by(token = orderId).first()
			if order is not None:
				if order.paystate == 7:
					state = 'successful'
					order.paytime = datetime.now()
					if orderScores == '':
						reason = '支付成功'
						order.paystate = 2
					else:
						reason = '感谢您的支付和评价'
						order.paystate = 6
						order.scores = float(orderScores)
					db.session.commit()
				elif order.paystate == 1:
					state = 'fail'
					reason = '请等商家发起支付流程！'
				else :
					state = 'fail'
					reason = '订单状态异常'
			else :
				state = 'fail'
				reason = '无效的订单'
		else :
			state = 'fail'
			reason = '无效的用户'

	except Exception, e:
		print e
		state = 'fail'
		reason = '服务器异常'

	response = jsonify({
	                   'state':state,
	                   'reason':reason
	                   })
	return response

@orderList_route.route('/ratedOrder', methods = ['POST'])
def ratedOrder():
	try :
		customerToken = request.json['token']
		orderId = request.json['orderId']
		orderScores = request.json['orderScores']
		customer = get_customer_user_by_token(customerToken)
		if customer is not None:
			order = customer.order.filter_by(token = orderId).first()
			if order is not None:
				if order.paystate == 2:
					order.scores = float(orderScores)
					order.paystate = 6
					db.session.commit()
					state = 'successful'
					reason = '感谢您的评价'
				elif order.paystate == 6:
					state = 'fail'
					reason = '您已经评价过该订单了~'
				else :
					state = 'fail'
					reason = '订单状态异常'
			else :
				state = 'fail'
				reason = '无效的订单'
		else :
			state = 'fail'
			reason = '无效的用户'
	except Exception, e:
		print e
		state = 'fail'
		reason = '服务器异常'

	response = jsonify({
	                   'state':state,
	                   'reason':reason
	                   })
	return response






