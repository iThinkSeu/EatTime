#-*- coding: UTF-8 -*-

from flask import Blueprint
from flask import request,jsonify,json
import traceback
import sys
sys.path.append("..")
from models import *

editUserInfo_route = Blueprint('editUserInfo', __name__)

@editUserInfo_route.route('/editUserInfo', methods=['POST'])
def editUserInfo():
    try:
        token = request.json['token']
        user = User.query.filter_by(token =token).first()
        if user is None:
            state = "fail"
            reason = "用户不存在"
            return jsonify({
                "state":state,
                "reason":reason
            })

        location = request.json.get("location")
        if request.json.get("location") != None:
            user.location = location

        if request.json.get("personprice") != None:
            user.personprice = float(request.json.get("personprice"))

        if request.json.get("scoles") != None:
            user.scoles = float(request.json.get("scoles"))

        if request.json.get("confirm") != None:
            user.confirm = int(request.json.get("confirm"))

        #db.session.add(user)
        db.session.commit()
        state = "sucessfull"
        reason = ""
        return jsonify({
            "state":state,
            "reason":reason
        })

    except Exception, e:
        print e
        state = "fail"
        reason="服务器异常"
        return jsonify({
            "state":state,
            "reason":reason
        })
