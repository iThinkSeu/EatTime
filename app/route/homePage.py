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
    customerUser = get_customer_usr_by_token(token)
    if customerUser is not None:
      pageitems = customerUser.paginate(page, per_page = 3, error_out = False)
      sellerView = [{'userid':item.id, 'name':item.username, 'location':item.location, 'monthsales':item.beordered.filter_by(paystate = 8, paytime + timedelta(days=30) > datetime.now()).all().foodincludes.count(), 'scores':item.scores, 'personprice':item.personprice, 'foodurl':'', 'headimg':''} for item in pageitems.items]
      bannerImgUrls = []
      state = 'successful'
      reason = ''
      response = jsonify({'state':state,
            'reason':reason,
            'bannerImgUrls': bannerImgUrls
            'result': sellerView})
      return reponse
    else:
      state = 'fail'
      reason = 'unvalid user'
      bannerImgUrls = []
      sellerView = []
      response = jsonify({'state':state,
            'reason':reason,
            'bannerImgUrls': bannerImgUrls
            'result': sellerView})
      return reponse
  except Exception ,e:
    print e
    state = 'fail'
    reason = 'e'
    bannerImgUrls = []
    sellerView = []
    response = jsonify({'state':state,
          'reason':reason,
          'bannerImgUrls': bannerImgUrls
          'result': sellerView})
    return reponse
