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

customerHomePage_route = Blueprint('customerHomePage', __name__)

@customerHomePage_route.route("/customerHomePage", methods=['POST'])
def homePage():
  try:
    token = request.json['token']
    page = request.json['page']
    customer = get_customer_user_by_token(token)
    if customer is not None:
      pageitems = User.query.order_by(User.scoles.asc()).paginate(page, per_page = 3, error_out = False)
      foodurl = ''
      headimg = ''
      sellerView = [{'userid':item.id, 'name':item.username, 'location':item.location, 'monthsales':sum([fitem.monthsales for fitem in item.foods]), 'scores':item.scoles, 'personprice':item.personprice, 'foodurl':foodurl, 'headimg':headimg} for item in pageitems.items]
      bannerImgUrls = []
      state = 'successful'
      reason = ''
      response = jsonify({'state':state,
            'reason':reason,
            'bannerImgUrls': bannerImgUrls,
            'result': sellerView})
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
