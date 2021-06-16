from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin
from . import login_manager
from sqlalchemy import desc

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

    
class User(UserMixin, db.Model):
    '''Class to define a user of the application.
    '''
    __tablename__ = "users"

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
    liked = db.relationship('PitchLike', foreign_keys='PitchLike.user_id', backref='user', lazy='dynamic')
    liked_comments = db.relationship('CommentLike', foreign_keys='CommentLike.user_id', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute.')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pass_secure, password)

    # Likes

    def like_pitch(self, pitch):
        if not self.has_liked_pitch(pitch):
            like = PitchLike(user_id=self.id, pitch_id=pitch.id)
            db.session.add(like)

    def unlike_pitch(self, pitch):
        if self.has_liked_pitch(pitch):
            PitchLike.query.filter_by(user_id = self.id, pitch_id = pitch.id).delete()

    def has_liked_pitch(self, pitch):
        return PitchLike.query.filter(PitchLike.user_id == self.id, PitchLike.pitch_id == pitch.id).count() > 0 

    def like_comment(self, comment):
        if not self.has_liked_comment(comment):
            like = CommentLike(user_id=self.id, comment_id=comment.id)
            db.session.add(like)

    def unlike_comment(self, comment):
        if self.has_liked_comment(comment):
            CommentLike.query.filter_by(user_id = self.id, comment_id = comment.id).delete()

    def has_liked_comment(self, comment):
        return CommentLike.query.filter(CommentLike.user_id == self.id, CommentLike.comment_id == comment.id).count() > 0 

class Pitch(db.Model):
    __tablename__ = "pitches"

    id = db.Column(db.Integer, primary_key = True)
    posted = db.Column(db.DateTime, default=datetime.utcnow)
    # likes = db.Column(db.Integer, default=0)
    # dislikes = db.Column(db.Integer, default=0)
    pitch = db.Column(db.String())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    comments = db.relationship('Comment', backref='pitch', lazy='dynamic')
    likes = db.relationship('PitchLike', backref='pitch', lazy='dynamic')

    def save_pitch(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_pitches(cls):
        pitches = Pitch.query.order_by(desc(Pitch.posted)).all()
        return pitches

    @classmethod
    def get_pitches_by_category(cls, id):
        pitches = Pitch.query.filter_by(category_id=id).all()
        return pitches

    @classmethod
    def get_pitches_by_user(cls, id):
        pitches = Pitch.query.filter_by(user_id=id).all()
        return pitches
        

class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String())
    posted = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    pitch_id = db.Column(db.Integer, db.ForeignKey('pitches.id'))
    likes = db.relationship('CommentLike', backref='comment', lazy='dynamic')

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls, id):
        comments = Comment.query.filter_by(pitch_id=id)
        return comments
        
class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(255))
    name = db.Column(db.String(255))

    pitches = db.relationship('Pitch', backref='category', lazy='dynamic')

    def __repr__(self):
        return self.id

class PitchLike(db.Model):
    __tablename__ = 'pitch_likes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    pitch_id = db.Column(db.Integer, db.ForeignKey('pitches.id'))

class CommentLike(db.Model):
    __tablename__ = 'comment_likes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    

