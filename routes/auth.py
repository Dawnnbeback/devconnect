from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from models.user import User
from models import db
from models.post import Post

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('post.feed'))
        flash('Invalid username or password')
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')

@auth_bp.route('/user/<int:user_id>/follow', methods=['POST'])
@login_required
def follow(user_id):
    user = User.query.get_or_404(user_id)
    if current_user in user.followers:
        user.followers.remove(current_user)
        following = False
    else:
        user.followers.append(current_user)
        following = True
    db.session.commit()
    return jsonify({'success': True, 'following': following})

@auth_bp.route('/user/<int:user_id>')
def profile(user_id):
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id=user_id).order_by(Post.created_at.desc()).all()
    total_likes = sum(len(post.likes) for post in user.posts)
    return render_template('profile/view.html', user=user, posts=posts, total_likes=total_likes)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
