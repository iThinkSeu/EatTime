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

from route.uploadimage import uploadImage_route
app = create_app()



##注册蓝本路由
app.register_blueprint(loginRegister_route)  			#注册与登录
app.register_blueprint(publishFood_route)				#
app.register_blueprint(orderList_route)
app.register_blueprint(homePage_route)

app.register_blueprint(personInfo_route)
app.register_blueprint(userInfo_route)
app.register_blueprint(editUserInfo_route)
app.register_blueprint(editFood_route)

#图片上传
app.register_blueprint(uploadImage_route)

if __name__ == '__main__':
	app.run(host=os.getenv('IP','0.0.0.0'),port=int(os.getenv('PORT',3000)),debug = True)



