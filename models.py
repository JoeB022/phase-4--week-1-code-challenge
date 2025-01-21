from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import MetaData,ForeignKey,DateTime
from datetime import date
# initializing metadata 
metadata = MetaData 

#setting up sql db
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    email=db.Column(db.String(128), nullable=False, unique=True)
    is_approved = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)

    password=db.Column(db.String(128), nullable=False)
    orders = db.relationship('Order', back_populates='user', lazy=True)
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))  
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    stock_quantity = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String(255))

class Order(db.Model): 
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    order_date = db.Column(db.DateTime,nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    order_status = db.Column(db.String(20), default='Pending') 


    user = db.relationship('User', back_populates='orders', lazy=True)