#-*- coding: UTF-8 -*-

from flask import Blueprint
from flask import request,jsonify,json
import traceback
import sys
sys.path.append("..")
from models import customerUser
from functions.DBFunctions import *
from sqlalchemy import or_
from sqlalchemy import and_
#from flask.ext.cache import Cache



personInfo_route = Blueprint('personInfo', __name__)
#cache = Cache(personInfo_route, config={'CACHE_TYPE': 'simple'})


@personInfo_route.route('/personInfo', methods=['POST'])
#@cache.cached(timeout=50, key_prefix='cached_psnInfo_')
def personInfo():
    emptyDic = {
         "friendly":"",
         "honesty":"",
         "passion":""}

    try:
        token = request.json['token']
        user = customerUser.query.filter_by(token =token).first()
        #没有用户信息
        print "personInfo: " + token
        if user is None:
             errorDic = {"state":"fail",
                         "reason":"没有此用户"}
             errorDic = dict(errorDic,**emptyDic)
             return jsonify(errorDic)

        validOrders = user.order.filter(or_('paystate = 6' , 'paystate = 2')).order_by(orderList.paytime.desc()).limit(30).all()
        cancelNum = 0.1
        freeNum = 0.1
        discountPrice = 0.1
        totalPrice = 0.1
        number = 0.1
        for item in validOrders:
            number += 1
            if item.paystate == 4:
                cancelNum += 1
            if item.discount == 0:
                freeNum += 1
            totalPrice += item.price
            discountPrice += item.payprice

        user.friendly = 60 + freeNum / max(1,number) * 40
        user.honesty = 100 - cancelNum / max(1,number) * 100
        user.passion = 60 + (totalPrice - discountPrice) / max(1,number) * 40
        db.session.commit()

        friendly = user.friendly
        honesty = user.honesty
        passion = user.passion

        state = "successful"
        reason = ""
        return jsonify({"state":state,
                     "reason":reason,
                     "friendly":friendly,
                     "honesty":honesty,
                     "passion":passion})

    except Exception, e:
        print e
        errorDic = {"state":"fail",
                    "reason":"服务器异常"}
        errorDic = dict(errorDic,**emptyDic)
        return jsonify(errorDic)


@personInfo_route.route('/sellerInfo', methods = ['POST'])
def sellerInfo():
    try :
        sellerToken = request.json['token']
        seller = get_user_by_token(sellerToken)
        if seller is not None:
            state = 'successful'
            reason = ''
            sellerName = seller.nickname if seller.nickname is not None else ''
            sellerId = seller.id
            headImg = seller.headimgurl
            confirm = seller.confirm
        else:
            state = 'fail'
            reason = '无效的用户'
            headImg = ''
            confirm = ''
            sellerName = ''
            sellerId = ''
    except Exception, e:
        print e
        state = 'fail'
        reason = '服务器异常'
        headImg = ''
        confirm = ''
        sellerName = ''
        sellerId = ''
    response = jsonify({
                       'state':state,
                       'reason':reason,
                       'headImg':headImg,
                       'confirm':str(int(confirm)),
                       'sellerName':sellerName,
                       'sellerId':sellerId
                       })

    return response
