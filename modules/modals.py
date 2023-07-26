from modules import db,login_manager
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User_mgmt.query.get(int(user_id))

class Follow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('user_mgmt.id'), nullable=False)
    followed_id = db.Column(db.Integer, db.ForeignKey('user_mgmt.id'), nullable=False)


class User_mgmt(UserMixin, db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(15),nullable=False,unique=True)
    email = db.Column(db.String(50),nullable=False,unique=True)
    password = db.Column(db.String(80),nullable=False)
    image_file = db.Column(db.String(20),nullable=False,default='default.jpg')
    bg_file = db.Column(db.String(20),nullable=False,default='default_bg.jpg')
    bio = db.Column(db.String(200))
    date = db.Column(db.String(20))
    bday = db.Column(db.String(10))
    reset_token = db.Column(db.String(100))
    token_expiration = db.Column(db.DateTime)  

    posts = db.relationship('Post',backref='author',lazy=True)
    retwitted = db.relationship('Retweet',backref='retwitter',lazy=True)
    bookmarked = db.relationship('Bookmark',backref='saved_by',lazy=True)

    followers = db.relationship('Follow', foreign_keys=[Follow.followed_id], backref='followed', lazy='dynamic')
    following = db.relationship('Follow', foreign_keys=[Follow.follower_id], backref='follower', lazy='dynamic')

    def is_following(self, user):
        return self.following.filter_by(followed_id=user.id).first() is not None
    def unfollow(self, user):
        if self.is_following(user):
            follow_relationship = self.following.filter_by(followed_id=user.id).first()
            db.session.delete(follow_relationship)
            db.session.commit()
    def follow(self, user):
        if not self.is_following(user):
            follow_relationship = Follow(follower_id=self.id, followed_id=user.id)
            db.session.add(follow_relationship)
            db.session.commit()
    @property
    def followers_count(self):
        return self.followers.count()



class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    tweet = db.Column(db.String(500),nullable=False)
    stamp = db.Column(db.String(20),nullable=False)
    post_img = db.Column(db.String(20))
    user_id = db.Column(db.Integer,db.ForeignKey('user_mgmt.id'),nullable=False)

    retweets = db.relationship('Retweet',backref='ori_post',lazy=True)
    timeline = db.relationship('Timeline',backref='from_post',lazy=True)
    bookmark = db.relationship('Bookmark',backref='saved_post',lazy=True)

class Retweet(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    tweet_id = db.Column(db.Integer,db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('user_mgmt.id'),nullable=False)
    retweet_stamp = db.Column(db.String(20),nullable=False)
    retweet_text = db.Column(db.String(500),nullable=False)

    timeline = db.relationship('Timeline',backref='from_retweet',lazy=True)

class Timeline(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    post_id = db.Column(db.Integer,db.ForeignKey('post.id'),default=None)
    retweet_id = db.Column(db.Integer,db.ForeignKey('retweet.id'),default=None)

class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'),default=None)
    user_id = db.Column(db.Integer, db.ForeignKey('user_mgmt.id'),default=None)