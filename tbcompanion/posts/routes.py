from flask import Blueprint, render_template, request, url_for
from flask.helpers import flash
from flask_login import current_user
from flask_login.utils import login_required
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from tbcompanion import db
from tbcompanion.models import Post
from tbcompanion.posts.forms import PostForm

posts = Blueprint('posts', __name__)


@posts.route('/post/<int:post_id>', methods=['GET'])
def post(post_id):
	"""This page displays a post."""
	post_query = Post.query.get_or_404(post_id)
	return render_template('post_view.html', post=post_query)


@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def post_form():
	"""This is the page for creating a new post."""

	form = PostForm()

	if form.validate_on_submit():
		new_post = Post(
			title=form.title.data, 
			content=form.content.data, 
			author=current_user,
			project_id=form.project_id.data)

		db.session.add(new_post)
		db.session.commit()

		flash('You have published your post!', 'success')
		return redirect(url_for('main.home'))

	return render_template('post_form.html', form=form, title='New Post')


@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
	"""This is the page for updating an already-existing post."""

	post_query = Post.query.get_or_404(post_id)

	if post_query.author != current_user:  # Only the post's author can edit it..
		abort(403)

	form = PostForm()

	if form.validate_on_submit():
		post_query.title = form.title.data
		post_query.content = form.content.data

		db.session.commit()

		flash('You have updated your post!', 'success')
		return redirect(url_for('posts.post', post_id=post_query.id))

	elif request.method == 'GET':  # Fill in form fields with the posts' content.
		form.title.data = post.title
		form.content.data = post.content

	return render_template('post_form.html', form=form, title='New Post')


@posts.route('/post/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
	"""This is the route that deletes posts."""

	post_query = Post.query.get_or_404(post_id)

	if post_query.author != current_user:  # Only the post's author can delete it.
		print(current_user)
		abort(403)

	db.session.delete(post_query)
	db.session.commit()

	flash('You have deleted your post!', 'danger')
	return redirect(url_for('main.home'))
