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
	orderid = db.Column(db.Integer,db.ForeignKey('customerusers.id'),primary_key=True)
	orderedid = db.Column(db.Integer,db.ForeignKey('users.id'), primary_key=True)
	ordertime = db.Column(db.DateTime, default = datetime.now)
	peoplenumber = db.Column(db.Integer)
	price = db.Column(db.Float)
	payprice = db.Column(db.Float)
	paystate = db.Column(db.Boolean)
	paytime = db.Column(db.DateTime)
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
	def addfood(self,food):
		try:
			lp = orderListDetail(orderlistid = self.id, foodid = food.id)
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
	measuredatas = db.relationship('Measuredata',backref = 'instrument', lazy = 'dynamic')
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
	def publishmeasuredata(self,measuredata):
		try:
			measuredata.instrument = self
			db.session.add(measuredata)
			db.session.execute('set names utf8mb4')
			db.session.commit()
			return 0
		except Exception, e:
			print e
			db.session.rollback()
			return 2	
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
class customerUser(db.Model):
	__tablename__ = "customerusers"
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(32),unique = True)
	password = db.Column(db.String(32))
	token = db.Column(db.String(32))
	test = db.Column(db.String(32))
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
	def orderuser(self,user):
		try:
			lp = orderList(orderid = self.id, orderedid = user.id)
			db.session.add(lp)
			db.session.commit()
			return 0
		except Exception, e:
			print e
			db.session.rollback()
			return 2

class Measuredata(db.Model):
	__tablename__ = "messuredatas"
	id = db.Column(db.Integer,primary_key = True)
	instrumentid = db.Column(db.Integer,db.ForeignKey('users.id'))
	datatype = db.Column(db.String(32))
	value = db.Column(db.Float)
	timestamp = db.Column(db.DateTime, default = datetime.now)
	def add(self):
		try:
			db.session.add(self)
			db.session.execute('set names utf8mb4')
			db.session.commit()
		except Exception, e:
			print e
			db.session.rollback()
			return 2

class food(db.Model):
	__tablename__ = "foods"
	id = db.Column(db.Integer,primary_key = True)
	authorid = db.Column(db.Integer,db.ForeignKey('users.id'))
	name = db.Column(db.String(32))
	discription = db.Column(db.String(256))
	price = db.Column(db.Float)
	timestamp = db.Column(db.DateTime, default = datetime.now)
	monthsales = db.Column(db.Integer)
	#哪些订单包含这个食物
	whatlists =  db.relationship('orderListDetail', foreign_keys = [orderListDetail.foodid], backref = db.backref('foods', lazy='joined'), lazy='dynamic', cascade = 'all, delete-orphan')	
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







