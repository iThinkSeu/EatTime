#-*- coding: UTF-8 -*-
from flask import Blueprint
from flask import request,jsonify,json
import traceback
import sys
sys.path.append("..")
from models import *

publishFood_route = Blueprint('publishFood', __name__)

@publishFood_route.route('/publishFood', methods=['POST'])
def publishFood():
  try:
    token = request.json['token']
    sellerName = request.json.get('userName','')
    foodName = request.json['foodName']
    description = request.json['description']
    price = request.json['price']

