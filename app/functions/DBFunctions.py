#-*- coding: UTF-8 -*-
import sys
sys.path.append("..")
from models import *

def get_user_by_token(token):
	u=User.query.filter_by(token=token).first()
	return u
def get_user_by_username(username):
	u=User.query.filter_by(username=username).first()
	return u
def get_user_by_id(id):
	u=User.query.filter_by(id=id).first()
	return u
#获取customerUser 表相关函数
def get_customer_user_by_token(token):
	u=customerUser.query.filter_by(token=token).first()
	return u
def get_customer_user_by_username(username):
	u=customerUser.query.filter_by(username=username).first()
	return u
def get_customer_user_by_id(id):
	u=customerUser.query.filter_by(id=id).first()
	return u

def get_food_by_id(id):
	f = food.query.filter_by(id=id).first()
	return f

def get_food_by_name(foodName):
	f = food.query.filter_by(name=foodName).first()
	return f
