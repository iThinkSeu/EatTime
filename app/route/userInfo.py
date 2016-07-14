#-*- coding: UTF-8 -*-

from flask import Blueprint
from flask import request,jsonify,json
import traceback
import sys
sys.path.append("..")
from models import User
from models import food as Food

#说明：客户端发送:page（可选）,token
userInfo_route = Blueprint('userInfo', __name__)

@userInfo_route.route('/userInfo', methods=['POST'])
def userInfo():
    perPageCount = 5
    emptyDic = {
        "username":"",
        "homeimgurl":"",
        "confirm":"",
        "foodlist":"",
        "headimgurl":"",
        "location" : ""
    }
    try:
        token = request.json['token']
        #customerToken = request.json['customerToken']
        user = User.query.filter_by(token =token).first()
        print token
        if user is None:
            errorDic = {"state":"fail",
                        "reason":"用户不存在"}
            errorDic = dict(errorDic,**emptyDic)
            return jsonify(errorDic)

        username = user.nickname
        homeImgUrl = user.homeimgurl
        isconfirm = user.confirm
        headimgurl = user.headimgurl
        location = user.location
        #若有page,做分页；
        page = request.json.get("page")
        if page is None:

            foods = user.foods
        else:
            page = int(page)
            foods = user.foods.paginate(page =page,per_page = perPageCount,error_out=False)
            foods = foods.items

        foodList = []
        for food in foods:
            if food.disable == 1:
                continue
            if food.foodimgs.first() is None:
                imgurl =""
            else:
                imgurl = food.foodimgs.first().imageurl
            foodDic = {"foodid":food.id,
                        "foodname":food.name,
                        "monthSales":food.monthsales,
                        "price":food.price,
                        "description":food.description,
                        "imgurl": imgurl}
            foodList.append(foodDic)

        #成功返回return
        state = "successful"
        reason = ""
        return jsonify({
            "state":state,
            "reason":reason,
            "username":username,
            "homeimgurl":homeImgUrl,
            "confirm":isconfirm,
            "foodlist":foodList,
            "headimgurl":headimgurl,
            "location":location})

    except Exception, e:
        print e
        errorDic = {"state":"fail",
                    "reason":"服务器异常"}
        errorDic = dict(errorDic,**emptyDic)
        return jsonify(errorDic)
