#-*- coding: UTF-8 -*-

from flask import Blueprint
from flask import request,jsonify,json
import traceback
import sys
sys.path.append("..")
from models import customerUser
from main import memCache

personInfo_route = Blueprint('personInfo', __name__)

@cache.cached(timeout=50, key_prefix='cached_psnInfo_')
@personInfo_route.route('/personInfo', methods=['POST'])
def personInfo():
    emptyDic = {
         "friendly":"",
         "honesty":"",
         "passion":""}

    try:
        token = request.json['token']
        user = customerUser.query.filter_by(token =token).first()
        #没有用户信息
        if user is None:
             errorDic = {"state":"fail",
                         "reason":"没有此用户"}
             errorDic = dict(errorDic,**emptyDic)
             return jsonify(errorDic)

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
        errorDic = {"state":"fail",
                    "reason":"服务器异常"}
        errorDic = dict(errorDic,**emptyDic)
        return jsonify(errorDic)