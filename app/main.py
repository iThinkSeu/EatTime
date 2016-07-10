#-*- coding: UTF-8 -*-
from flask import request
from flask import render_template
from flask import redirect
from models import *
from wtforms import Form,TextField,PasswordField,validators
from hashmd5 import *
import os, stat
#from PIL import Image
#import Image
import shutil
import string;
import datetime
from dbSetting import create_app,db

from route.loginRegister import loginRegister_route
from route.publishFood import publishFood_route

app = create_app()

##注册蓝本路由
app.register_blueprint(loginRegister_route)  			#注册与登录
app.register_blueprint(publishFood_route)


if __name__ == '__main__':
	app.run(host=os.getenv('IP','0.0.0.0'),port=int(os.getenv('PORT',8080)),debug = True)



