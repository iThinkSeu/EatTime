#-*- coding: UTF-8 -*-

from flask import Blueprint
from flask import request,jsonify,json
import traceback
import sys
sys.path.append("..")
from models import User,db
from models import food as Food

confirmUser_route = Blueprint('confirmUser', __name__)

@confirmUser_route.route('/confirmUser', methods=['POST'])
def confirmUser():
    try:
        token = request.json['token']
        user = User.query.filter_by(token =token).first()
        if user is None:
            errorDic = {"state":"fail",
                        "reason":"用户不存在"}
            return jsonify(errorDic)
        user.nickname = request.json.get("username","")
        print user.nickname
        user.identity = str(request.json.get("userIdentity",""))
        user.location = request.json.get("userLocation","")
        user.altitude = float(request.json.get("latitude",0))
        user.logitude = float(request.json.get("longitude",0))
        if request.json.get("userSex") is None:
            pass
        else:
            user.sex = request.json["userSex"]
        db.session.add(user)
        db.session.commit()

        return jsonify({
            "state":"sucessful",
            "reason":""})
    except Exception,e:
        print e
        return jsonify({
            "state":"fail",
            "reason":"服务器异常"
        })
