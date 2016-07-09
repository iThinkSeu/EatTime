#-*- coding: UTF-8 -*- 
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#sqlurl = "mysql://root:root@127.0.0.1:3306/dataserverble?charset=utf8"
sqlurl = "mysql://root:root@119.29.233.72:3306/dataserverble?charset=utf8"
#sqlurl = "mysql://root:0596@223.3.36.246:3306/flasktestdb?charset=utf8"
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI']=sqlurl
    db.init_app(app)
    return app
