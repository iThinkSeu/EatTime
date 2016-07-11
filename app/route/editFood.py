from flask import Blueprint
from flask import request,jsonify,json
import traceback
import sys
sys.path.append("..")
from ..models import User
from ..models import food as Food


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
            food.description = str(request.json["foodDescription"])

        if request.json.get("foodPrice") is None:
            pass
        else:
            food.price = float(request.json["foodPrice"])

        imgUrlList = request.json.get("imgUrlList")
        if imgUrlList is None:
            pass
        else:




