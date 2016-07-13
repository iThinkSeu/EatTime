#-*- coding: UTF-8 -*-
from flask import Blueprint
from flask import request,jsonify,json
import traceback
import sys
sys.path.append("..")
from models import *
from functions.DBFunctions import *

publishFood_route = Blueprint('publishFood', __name__)

@publishFood_route.route('/publishFood', methods = ['POST'])
def publishFood():
  try:
    token = request.json['token']
    foodName = request.json['foodName']
    description = request.json.get('description','该商家很懒，并没有添加描述~')
    price = float(request.json['price'])

    seller = get_user_by_token(token)
    if seller is None:
      state = 'fail'
      reason = '无效的用户'
      foodId = ''
    else:
      newFood = food(authorid = seller.id, name = foodName, description = description, price = price, disable = 0, monthsales = 0)
      if seller.publishfood(newFood) == 0:
        state = 'successful'
        reason = ''
        foodId = str(newFood.id)
      else :
        state = 'fail'
        reason = '数据库异常'
        foodId = ''

  except Exception, e:
    #print 'Need Token!'
    print e
    state = 'fail'
    reason = '服务器异常'
    foodId - ''
  response = jsonify({'state':state,
                       'reason':reason,
                       'foodId':foodId})

  return response



