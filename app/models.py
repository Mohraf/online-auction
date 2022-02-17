from email.policy import default
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))


class ItemPhoto(db.Model):
    __tablename__ = 'item_photos'
    id = db.Column(db.Integer,primary_key = True)
    pic_path = db.Column(db.String())
    item_id = db.Column(db.Integer,db.ForeignKey("auction_items.id"))


class AuctionItem(db.Model):
    __tablename__ = 'auction_items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.String())
    image_path = db.Column(db.String())
    starting_price = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    photos = db.relationship('ItemPhoto',backref = 'auction_item',lazy = "dynamic")
    upvote = db.relationship('Upvote',backref='auction_item',lazy='dynamic')
    downvote = db.relationship('Downvote',backref='auction_item',lazy='dynamic')
    comment = db.relationship('Comment', backref='auction_item', lazy='dynamic')

    def save_item(self):
        db.session.add(self)
        db.session.commit()
    

    @classmethod
    def get_items(cls):
        items = AuctionItem.query.all()
        return items
    

    def get_item(cls, id):
        item = AuctionItem.query.filter_by(user_id=id).all()


class PhotoProfile(db.Model):
    __tablename__ = 'profile_photos'

    id = db.Column(db.Integer,primary_key = True)
    pic_path = db.Column(db.String())
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))


class User(UserMixin, db.Model):
  __tablename__ = 'users'

  id = db.Column(db.Integer,primary_key = True)
  username = db.Column(db.String(255),index = True)
  email = db.Column(db.String(255),unique = True,index = True)
  role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
  bio = db.Column(db.String(255))
  profile_pic_path = db.Column(db.String())


  password_hash = db.Column(db.String(255))
  photos = db.relationship('PhotoProfile',backref = 'user',lazy = "dynamic")
  upvote = db.relationship('Upvote',backref='user',lazy='dynamic')
  downvote = db.relationship('Downvote',backref='user',lazy='dynamic')
  comment = db.relationship('Comment', backref='user', lazy='dynamic')
#   reviews = db.relationship('Review',backref = 'user',lazy = "dynamic")

  @property
  def password(self):
      raise AttributeError('You cannnot read the password attribute')

  @password.setter
  def password(self, password):
      self.password_hash = generate_password_hash(password)


  def verify_password(self,password):
      return check_password_hash(self.password_hash,password)


  def save_user(self):
      db.session.add(self)
      db.session.commit()

  def __repr__(self):
      return f'User {self.username}'


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return f'user {self.name}'


class Upvote(db.Model):
    __tablename__ = "upvotes"

    id = db.Column(db.Integer,primary_key=True)
    auction_id = db.Column(db.Integer,db.ForeignKey("auction_items.id"))
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_upvotes(cls,id):
        upvote = Upvote.query.filter_by(auction_id=id).all()
        return upvote


    def __repr__(self):
        return f'{self.user_id}:{self.auction_id}'
class Downvote(db.Model):
    __tablename__ = "downvotes"

    id = db.Column(db.Integer,primary_key=True)
    auction_id = db.Column(db.Integer,db.ForeignKey("auction_items.id"))
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
   
    def save(self):
        db.session.add(self)
        db.session.commit()
    @classmethod
    def get_downvotes(cls,id):
        downvote = Downvote.query.filter_by(auction_id=id).all()
        return downvote

    def __repr__(self):
        return f'{self.user_id}:{self.auction_id}'


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text())
    auction_id = db.Column(db.Integer,db.ForeignKey("auction_items.id"))
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls,id):
        comments = Comment.query.filter_by(auction_id=id).all()

        return comments

    
    def __repr__(self):
        return f'comment:{self.comment}'