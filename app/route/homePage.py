#-*- coding: UTF-8 -*-
from flask import Blueprint
from flask import request,jsonify,json
import traceback
import math
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
  db.session.commit()

  #位置排序时，返回的商家数量
  backCount = 20
  try:
    token = request.json['token']
    page = request.json['page']
    customer = get_customer_user_by_token(token)
    if customer is not None:
      #没有位置信息，按照评价排序
      if request.json.get("latitude") is None or request.json.get("longitude") is None:
          pageitems = User.query.order_by(User.scoles.asc()).paginate(int(page), per_page = 10, error_out = False).items
      else:
          user_distance = ordey_by_distance(float(request.json["latitude"]),float(request.json["longitude"]))
          count = 0
          users = []
          distance = []
          for item in user_distance:
              users.append(item[0])
              distance.append(item[1])
          pageitems = users
          if len(users) < backCount:
              backCount = len(users)

      sellerView = [{'sellerId':item.token, 'sellerName':item.nickname, 'location':item.location if item.location is not None else '', 'monthSales':sum([fitem.monthsales for fitem in item.foods]), 'scores':item.scoles, 'personPrice':item.personprice, 'foodImg':item.foods.first().foodimgs.first().imageurl if item.foods.first() is not None and item.foods.first().foodimgs.first() is not None else '', 'headImg':item.headimgurl if item.headimgurl is not None else ''} for item in pageitems]

      #收到坐标位置，添加返回字段distance
      if request.json.get("latitude") is None and request.json.get("longitude") is None:
            pass
      else:
            for i in range(backCount):
                temp = {"distance":distance[i]}
                item = sellerView[i]
                item=dict(item.items()+temp.items())
                sellerView[i] = item

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
    db.session.commit()
    sellerToken = request.json['token']
    page = int(request.json['page'])
    seller = get_user_by_token(sellerToken)
    if seller is not None:
      #img = ''
      pageitems = seller.foods.paginate(page, per_page = 30, error_out = False)
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

def ordey_by_distance(lat,lng):
    user_distance= {}     #{user,distance}
    users = User.query.all()
    for user in users:
        if user.altitude is  None or user.logitude is  None:
            continue
        distance = getDistanceFromXtoY(user,lat, lng)
        temp = {user:distance}
        user_distance = dict(user_distance.items() + temp.items())
    a =10
    print user_distance
    user_distance = sorted(user_distance.iteritems(), key=lambda e:e[1], reverse=False)
    return user_distance

def getDistanceFromXtoY(user, lat_b,lng_b):
    lat_a = user.altitude
    lng_a = user.logitude
    pk = 180 / 3.14169
    a1 = lat_a / pk
    a2 = lng_a / pk
    b1 = lat_b / pk
    b2 = lng_b / pk
    t1 = math.cos(a1) * math.cos(a2) * math.cos(b1) * math.cos(b2)
    t2 = math.cos(a1) * math.sin(a2) * math.cos(b1) * math.sin(b2)
    t3 = math.sin(a1) * math.sin(b1)
    tt = math.acos(t1 + t2 + t3)
    return 6366000 * tt

