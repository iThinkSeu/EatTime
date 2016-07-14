#-*- coding: UTF-8 -*-
from flask import request
from flask import render_template
from flask import redirect
from models import *
from wtforms import Form,TextField,PasswordField,validators
from functions.hashmd5 import *
import os, stat
#from PIL import Image
#import Image
import shutil
import string;
import datetime
from dbSetting import create_app,db
from route.loginRegister import loginRegister_route
from route.publishFood import publishFood_route
from route.orderList import orderList_route
from route.homePage import homePage_route
from route.personInfo import personInfo_route
from route.userInfo import userInfo_route
from route.editUserInfo import editUserInfo_route
from route.editFood import editFood_route
from route.confirmUser import confirmUser_route
from route.uploadimage import uploadImage_route



app = create_app()  #创建应用




##注册蓝本路由
app.register_blueprint(loginRegister_route)  			#注册与登录
app.register_blueprint(publishFood_route)				#发布食物
app.register_blueprint(orderList_route)					#订单相关路由
app.register_blueprint(homePage_route)					#主页相关路由

app.register_blueprint(personInfo_route)				#个人信息路由
app.register_blueprint(userInfo_route)					#获取用户路由
app.register_blueprint(editUserInfo_route)				#编辑用户信息
app.register_blueprint(editFood_route)					#编辑食物信息路由
app.register_blueprint(confirmUser_route)				#商家信息认证路由

app.register_blueprint(uploadImage_route)				#图片上传 

if __name__ == '__main__':
	app.run(host=os.getenv('IP','0.0.0.0'),port=int(os.getenv('PORT',3000)),debug = True)



