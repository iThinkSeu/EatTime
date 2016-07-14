#-*- coding: UTF-8 -*-

from flask import Blueprint
from flask import request,jsonify,json
import traceback
import sys
sys.path.append("..")
from models import User, db, foodimage
from models import food as Food


editFood_route = Blueprint('editFood', __name__)
@editFood_route.route('/editFood', methods=['POST'])
def editFood():
    try:
        token = request.json['token']
        food_id =int(request.json.get("foodid"))
        user = User.query.filter_by(token =token).first()

        if food_id != None:
            food = Food.query.filter_by(id = food_id).first()
        else:
            food = None

        if user is None or food is None or food_id is None:
            state = "fail"
            reason="用户/菜不存在"
            return jsonify({
                "state":state,
                "reason":reason
            })

        if request.json.get("foodDescription") is None:
            pass
        else:
            food.description = (request.json["foodDescription"])

        if request.json.get("foodPrice") is None:
            pass
        else:
            food.price = float(request.json["foodPrice"])


        if request.json.get("disable") is None:
            print "nothing"
            pass
        else:
            disable = int(request.json.get("disable"))
            print disable
            if disable == 1:
                food.disable = 1
            else:
                food.disable = 0

        food.add()

        state = "successful"
        reason = ""
    except Exception, e:
        print e
        state = "fail"
        reason = "服务器异常"

    finally:
        return jsonify({
            "state":state,
            "reason":reason
        })






