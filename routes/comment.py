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
