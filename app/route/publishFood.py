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
    sellerName = request.json.get('userName','')
    foodName = request.json['foodName']
    description = request.json.get('description','该商家很懒，并没有添加描述~')
    price = request.json['price']

    seller = get_user_by_token(token)
    if seller is None:
      state = 'fail'
      reason = 'unvalid user'
    else:
      newFood = food(authorid = seller.id, name = foodName, description = description, price = price)
      if seller.publishfood(newFood) == 0:
        state = 'successful'
        reason = ''
      else :
        state = 'fail'
        reason = 'database error'
  except Exception, e:
    print 'Need Token!'
    print e
    state = 'fail'
    reason = 'need token'

  response = jsonify({'state':state,
                     'reason':reason})

  return response


