#-*- coding: UTF-8 -*-

from flask import Blueprint
from flask import request,jsonify,json
import traceback
import sys
sys.path.append("..")
from models import customerUser

personInfo_route = Blueprint('personInfo', __name__)

@personInfo_route.route('/personInfo', methods=['POST'])
def personInfo():
    state = "fail"
    reason = ""
    friendly = ""
    passion = ""
    honesty = ""

    try:
        token = request.json['token']
        user = customerUser.query.filter_by(token =token).first()
        #没有用户信息
        if user is None:
            state ="fail"
            reason = "没有这个用户"
            return jsonify({"state":state,
                             "reason":reason
                            })

        friendly = user.friendly
        honesty = user.honesty
        passion = user.passion

        state = "successful"
        reason = ""

    except Exception, e:
        state = "fail"
        reason = "服务器异常"


    return jsonify({"state":state,
                     "reason":reason,
                     "friendly":friendly,
                     "honesty":honesty,
                     "passion":passion
                        })