from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from models.post import Post
from models.comment import Comment
from models import db

post_bp = Blueprint('post', __name__)

@post_bp.route('/feed')
@login_required
def feed():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('posts/feed.html', posts=posts)

@post_bp.route('/post/<int:post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id):
    post = Post.query.get_or_404(post_id)
    content = request.form.get('content')
    
    comment = Comment(
        content=content,
        user_id=current_user.id,
        post_id=post_id
    )
    
    db.session.add(comment)
    db.session.commit()
    
    return redirect(url_for('post.view', post_id=post_id))

@post_bp.route('/post/<int:post_id>')
def view(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('posts/view.html', post=post)

@post_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        
        post = Post(
            title=title,
            content=content,
            user_id=current_user.id
        )
        
        db.session.add(post)
        db.session.commit()
        
        return redirect(url_for('post.feed'))
        
    return render_template('posts/create.html')