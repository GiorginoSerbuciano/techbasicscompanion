from flask import Blueprint, render_template, request, url_for
from flask.helpers import flash
from flask_login import current_user
from flask_login.utils import login_required
from tbcompanion import db
from tbcompanion.posts.forms import PostForm
from tbcompanion.models import Post
from werkzeug.exceptions import abort
from werkzeug.utils import redirect


posts = Blueprint('posts', __name__)

@posts.route('/post/<int:post_id>', methods=['GET'])
def post(post_id):
	post = Post.query.get_or_404(post_id)
	return render_template('post_view.html', post=post)

@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def post_form():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(
			title=form.title.data, 
			content=form.content.data, 
			post_author=current_user,
			project_id=form.project_id.data)
		db.session.add(post)
		db.session.commit()
		flash('You have published your post!', 'success')
		return redirect(url_for('main.home'))
	return render_template('post_form.html', form=form, title='New Post')

@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	form = PostForm()
	print('Entering validation conditional...')
	if form.validate_on_submit():
		post.title = form.title.data
		post.content = form.content.data
		db.session.commit()
		flash('You have updated your post!', 'success')
		print('Form validated!')
		return redirect(url_for('posts.post', post_id=post.id))
	elif request.method == 'GET':
		form.title.data = post.title
		form.content.data = post.content
		print('elif conditional: Filled in form fields!')
	return render_template('post_form.html', form=form, title='New Post')

@posts.route('/post/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		print(current_user)
		abort(403)
	db.session.delete(post)
	db.session.commit()
	flash('You have deleted your post!', 'danger')
	return redirect(url_for('main.home'))
