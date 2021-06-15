from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin
from . import login_manager
from sqlalchemy import asc, desc

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    
class User(UserMixin, db.Model):
    '''Class to define a user of the application.
    '''
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(255))
    fname = db.Column(db.String(255))
    lname = db.Column(db.String(255))
    bio = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, index=True)
    profile_pic_path = db.Column(db.String())
    pass_secure = db.Column(db.String(255))

    comments = db.relationship('Comment', backref='user', lazy='dynamic')
    pitches = db.relationship('Pitch', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute.')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pass_secure, password)

class Pitch(db.Model):
    __tablename__ = 'pitches'

    id = db.Column(db.Integer, primary_key = True)
    posted = db.Column(db.DateTime, default=datetime.utcnow)
    likes = db.Column(db.Integer, default=0)
    dislikes = db.Column(db.Integer, default=0)
    pitch = db.Column(db.String())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    comments = db.relationship('Comment', backref='pitch', lazy='dynamic')

    def save_pitch(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_pitches_by_category(cls, id):
        pitches = Pitch.query.filter_by(category_id=id).order_by(desc(Pitch.posted)).all()
        return pitches

    @classmethod
    def get_pitches_by_user(cls, id):
        pitches = Pitch.query.filter_by(user_id=id).all()
        return pitches

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String())
    likes = db.Column(db.Integer, default=0)
    dislikes = db.Column(db.Integer, default=0)
    posted = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    pitch_id = db.Column(db.Integer, db.ForeignKey('pitches.id'))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls, id):
        comments = Comment.query.filter_by(pitch_id=id).order_by(asc(Comment.posted)).all()
        return comments
        
class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(255))
    name = db.Column(db.String(255))

    pitches = db.relationship('Pitch', backref='category', lazy='dynamic')

    def __repr__(self):
        return self.id
    

