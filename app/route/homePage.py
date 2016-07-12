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

homePage_route = Blueprint('homePage', __name__)

@homePage_route.route("/customerHomePage", methods=['POST'])
def customerHomePage():
  try:
    token = request.json['token']
    page = request.json['page']
    customer = get_customer_user_by_token(token)
    if customer is not None:
      pageitems = User.query.order_by(User.scoles.asc()).paginate(int(page), per_page = 5, error_out = False)
      sellerView = [{'sellerId':item.token, 'sellerName':item.username, 'location':item.location if item.location is not None else '', 'monthSales':sum([fitem.monthsales for fitem in item.foods]), 'scores':item.scoles, 'personPrice':item.personprice, 'foodImg':item.foods.first().foodimgs.first().imageurl if item.foods.first() is not None and item.foods.first().foodimgs.first() is not None else '', 'headImg':item.headimgurl if item.headimgurl is not None else ''} for item in pageitems.items]
      bannerImgUrls = [{'imgUrls':item.imageurl, 'rank':item.rank} for item in topofficial.query.all()]
      state = 'successful'
      reason = ''
      response = jsonify({'state':state,
            'reason':reason,
            'bannerImgUrls': bannerImgUrls,
            'sellerView': sellerView})
      return response
    else:
      state = 'fail'
      reason = 'unvalid user'
      bannerImgUrls = []
      sellerView = []
      response = jsonify({'state':state,
            'reason':reason,
            'bannerImgUrls': bannerImgUrls,
            'result': sellerView})
      return response
  except Exception ,e:
    print e
    state = 'fail'
    reason = 'e'
    bannerImgUrls = []
    sellerView = []
    response = jsonify({'state':state,
          'reason':reason,
          'bannerImgUrls': bannerImgUrls,
          'result': sellerView})
    return response



@homePage_route.route("/sellerHomePage", methods = ['POST'])
def sellerHomePage():
  try:
    sellerToken = request.json['token']
    page = int(request.json['page'])
    seller = get_user_by_token(sellerToken)
    if seller is not None:
      #img = ''
      pageitems = seller.foods.paginate(page, per_page = 10, error_out = False)
      foodList = [{'foodId':str(item.id), 'foodName':item.name, 'foodMonthSales':str(item.monthsales), 'foodPrice':str(item.price), 'disable': str(1) if item.disable else str(0), 'foodImg': item.foodimgs.first().imageurl if item.foodimgs.first() is not None else ''} for item in pageitems.items]
      state = 'successful'
      reason = ''
    else :
      state = 'fail'
      reason = 'un valid seller'
      foodList = []

  except Exception, e:
    print e
    state = 'fail'
    reason = 'exception'
    foodList = []
  response = jsonify({'state':state,
                      'reason':reason,
                      'foodList':foodList
                      })

  return response
