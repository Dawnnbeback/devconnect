from datetime import datetime
from models import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    likes = db.relationship('User', secondary='post_likes', backref='liked_posts')
    comments = db.relationship('Comment', backref='parent_post', lazy=True)
    user = db.relationship('User', foreign_keys=[user_id])

post_likes = db.Table('post_likes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.UniqueConstraint('user_id', 'post_id', name='unique_user_post_like')
)
