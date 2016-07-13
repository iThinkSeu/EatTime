#-*- coding: UTF-8 -*-
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from datetime import *
from sqlalchemy import or_
from sqlalchemy import and_
from dbSetting import create_app,db,sqlurl


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']=sqlurl
db = SQLAlchemy(app)


#数据库升级时需要使用，平常不执行下面代码，创建app
if __name__ == '__main__':
	app = Flask(__name__)
	app.config['SQLALCHEMY_DATABASE_URI']=sqlurl
	db.init_app(app)
	migrage = Migrate(app,db)
	manager = Manager(app)
	manager.add_command('db',MigrateCommand)



#订单详情关系表
class orderListDetail(db.Model):
	__tablename__ = "orderListDetails"
	id = db.Column(db.Integer,primary_key = True)
	orderlistid = db.Column(db.Integer,db.ForeignKey('orderlists.id'),primary_key = True)
	foodid = db.Column(db.Integer,db.ForeignKey('foods.id'),primary_key = True)
	number = db.Column(db.Integer)
	timestamp = db.Column(db.DateTime,default = datetime.now)
	def add(self):
		try:
			db.session.add(self)
			db.session.execute('set names utf8mb4')
			db.session.commit()
		except Exception, e:
			print e
			db.session.rollback()
			return 2
#订单关系表
class orderList(db.Model):
	__tablename__ = "orderlists"
	id = db.Column(db.Integer,primary_key = True)
	token = db.Column(db.String(32))
	orderid = db.Column(db.Integer,db.ForeignKey('customerusers.id'),primary_key=True)
	orderedid = db.Column(db.Integer,db.ForeignKey('users.id'), primary_key=True)
	ordertime = db.Column(db.DateTime, default = datetime.now)
	peoplenumber = db.Column(db.Integer)
	price = db.Column(db.Float)
	payprice = db.Column(db.Float)
	paystate = db.Column(db.Integer)
	planeattime = db.Column(db.DateTime)
	paytime = db.Column(db.DateTime)
	scores = db.Column(db.Float, default = 0)
	discount = db.Column(db.Float, default = 10)
	#订单包含哪些食物
	foodincludes =  db.relationship('orderListDetail', foreign_keys = [orderListDetail.orderlistid], backref = db.backref('orderlist', lazy='joined'), lazy='dynamic', cascade = 'all, delete-orphan')
	def add(self):
		try:
			db.session.add(self)
			db.session.execute('set names utf8mb4')
			db.session.commit()
		except Exception, e:
			print e
			db.session.rollback()
			return 2
	def addfood(self,food,number):
		try:
			lp = orderListDetail(orderlistid = self.id, foodid = food.id, number = number)
			db.session.add(lp)
			db.session.commit()
			return 0
		except Exception, e:
			print e
			db.session.rollback()
			return 2
class User(db.Model):
	__tablename__ = "users"
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(32),unique = True)
	password = db.Column(db.String(32))
	token = db.Column(db.String(32))
	location = db.Column(db.String(32))
	scoles = db.Column(db.Float)
	personprice = db.Column(db.Float)
	confirm = db.Column(db.Boolean)
	homeimgurl = db.Column(db.String(256))
	headimgurl = db.Column(db.String(256))
	identity = db.Column(db.String(256))
	sex = db.Column(db.String(32))
	logitude = db.Column(db.Float)
	altitude = db.Column(db.Float)
	nickname = db.Column(db.String(32))
	cookLifeimgurl = db.Column(db.String(256))
	cookEnvirimgurl = db.Column(db.String(256))
	bestFoodimgurl = db.Column(db.String(256))
	foods = db.relationship('food',backref = 'foodauthor', lazy = 'dynamic')
	beordered =  db.relationship('orderList', foreign_keys = [orderList.orderedid], backref = db.backref('beordereduser', lazy='joined'), lazy='dynamic', cascade = 'all, delete-orphan')

	def add(self):
		try:
			tempuser = User.query.filter_by(username=self.username).first()
			if tempuser is None:
				db.session.add(self)
				db.session.commit()
				return 0
			else:
				return 1
		except Exception, e:
			print e
			db.session.rollback()
			return 2
	def isExisted(self):
		tempuser = User.query.filter_by(username=self.username,password=self.password).first()
		if tempuser is None:
			return 0
		else:
			return 1
	def isExistedusername(self):
		tempuser = User.query.filter_by(username = self.username).first()
		if tempuser is None:
			return 0
		else:
			return 1
	def publishfood(self,food):
		try:
			food.foodauthor = self
			db.session.add(food)
			db.session.execute('set names utf8mb4')
			db.session.commit()
			return 0
		except Exception, e:
			print e
			db.session.rollback()
			return 2
	def addchange(self):
		try:
			db.session.add(self)
			db.session.execute('set names utf8mb4')
			db.session.commit()
		except Exception, e:
			print e
			db.session.rollback()
class customerUser(db.Model):
	__tablename__ = "customerusers"
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(32),unique = True)
	password = db.Column(db.String(32))
	token = db.Column(db.String(32))
	honesty = db.Column(db.Float) #信誉度
	friendly = db.Column(db.Float)
	passion = db.Column(db.Float)
	logitude = db.Column(db.Float)
	altitude = db.Column(db.Float)
	order =  db.relationship('orderList', foreign_keys = [orderList.orderid], backref = db.backref('orderuser', lazy='joined'), lazy='dynamic', cascade = 'all, delete-orphan')

	def add(self):
		try:
			tempuser = User.query.filter_by(username=self.username).first()
			if tempuser is None:
				db.session.add(self)
				db.session.commit()
				return 0
			else:
				return 1
		except Exception, e:
			print e
			db.session.rollback()
			return 2
	def addchange(self):
		try:
			db.session.add(self)
			db.session.execute('set names utf8mb4')
			db.session.commit()
		except Exception, e:
			print e
			db.session.rollback()
			return 2
	def orderuser(self,user,peoplenumber,price,paystate):
		try:
			lp = orderList(orderid = self.id, orderedid = user.id, peoplenumber = peoplenumber, price = price,  paystate = paystate)
			db.session.add(lp)
			db.session.commit()
			return 0,lp
		except Exception, e:
			print e
			db.session.rollback()
			return 2,None

class food(db.Model):
	__tablename__ = "foods"
	id = db.Column(db.Integer,primary_key = True)
	authorid = db.Column(db.Integer,db.ForeignKey('users.id'))
	name = db.Column(db.String(32))
	description = db.Column(db.String(256))
	price = db.Column(db.Float)
	timestamp = db.Column(db.DateTime, default = datetime.now)
	monthsales = db.Column(db.Integer)
	disable = db.Column(db.Boolean,default = False) #表示食物是否有效，False=上架、True=下架
	#哪些订单包含这个食物
	whatlists =  db.relationship('orderListDetail', foreign_keys = [orderListDetail.foodid], backref = db.backref('foods', lazy='joined'), lazy='dynamic', cascade = 'all, delete-orphan')
	foodimgs = db.relationship('foodimage', backref = 'foods', lazy = 'dynamic')
	def add(self):
		try:
			db.session.add(self)
			db.session.execute('set names utf8mb4')
			db.session.commit()
		except Exception, e:
			print e
			db.session.rollback()
			return 2
	def addimage(self,imageurl):
		try:
			tmp = foodimage.query.filter_by(foodid = self.id,imageurl=imageurl).first()
			if tmp==None:
				f = foodimage(foodid = self.id,imageurl=imageurl)
				db.session.add(f)
				db.session.commit()
				return 0
			else:
				tmp.foodid = self.id
				imp.imageurl = imageurl
				tmp.add()
				return 1	
		except Exception, e:
			print e
			db.session.rollback()
			return 2	


class topofficial(db.Model):
	__tablename__ = 'topofficials'
	id = db.Column(db.Integer,primary_key=True)
	imageurl = db.Column(db.String(256))
	userid = db.Column(db.Integer)
	rank = db.Column(db.Integer,default = 0)
	def add(self):
		try:
			db.session.add(self)
			db.session.commit()
			return 0
		except Exception, e:
			print e
			db.session.rollback()
			return 2
class foodimage(db.Model):
	__tablename__ = 'foodimages'
	id = db.Column(db.Integer,primary_key=True)
	imageurl = db.Column(db.String(256))
	foodid = db.Column(db.Integer, db.ForeignKey('foods.id'))
	def add(self):
		try:
			db.session.add(self)
			db.session.commit()
			return 0
		except Exception, e:
			print e
			db.session.rollback()
			return 2
class checkMsg(db.Model):
	__tablename__ = 'checkMsgs'
	id = db.Column(db.Integer,primary_key = True)
	phone = db.Column(db.String(64))
	code = db.Column(db.String(32))
	timestamp = db.Column(db.DateTime,default = datetime.now)
	def add(self):
		try:
			db.session.add(self)
			db.session.execute('set names utf8mb4')
			db.session.commit()
		except Exception, e:
			print e
			db.session.rollback()
			return 2

def getuserinformation(token):
	u=User.query.filter_by(token=token).first()
	return u

def getTokeninformation(username):
	u=User.query.filter_by(username=username).first()
	return u

def get_history_data(typelist,start_time,end_time):
	a = Measuredata.query.filter(Measuredata.datatype.in_(typelist)).filter(Measuredata.timestamp.between(start_time,end_time)).order_by(Measuredata.timestamp.desc()).all()
	#a = Measuredata.query.filter(Measuredata.datatype.in_(typelist)).order_by(Measuredata.timestamp.desc()).all()
	return a

if __name__ == '__main__':
	manager.run()







