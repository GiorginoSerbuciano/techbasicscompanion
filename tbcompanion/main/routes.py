import os

from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from requests_oauthlib import OAuth2Session
from sqlalchemy import desc

from tbcompanion.main.forms import SearchBox
from tbcompanion.models import Post, Project, User

main = Blueprint('main', __name__)

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # Allows HTTP for testing.
client_id = os.environ.get('TBCOMP_CLIENT_ID')
client_secret = os.environ.get('TBCOMP_CLIENT_SECRET')
authorization_base_url = 'https://github.com/login/oauth/authorize'
token_url = 'https://github.com/login/oauth/access_token'


@main.route('/github_authorization')
def github_authorization():
	"""Access the Github app authorization page."""

	g = OAuth2Session(client_id)
	authorization_url, state = g.authorization_url(authorization_base_url)
	session['oauth_state'] = state  # Attack protection
	return redirect(authorization_url)


@main.route('/callback')
def callback():
	"""Callback from Github authorization."""

	g = OAuth2Session(client_id, state=session['oauth_state'])
	token = g.fetch_token(token_url,
						  client_secret=client_secret,
						  authorization_response=request.url)
	session['oauth_token'] = token
	return redirect(url_for('.home'))


@main.route('/github_profile/user', methods=['GET'])
def github_user_profile():
	"""An example of how to access a protected resource using an authorized session."""

	g = OAuth2Session(client_id, token=session['oauth_token'])  # token must be used for every definition of 'g'
	return jsonify(g.get('https://api.github.com/user').json())


@main.route('/', methods=['GET', 'POST'])
def home():
	"""Home page."""

	posts = Post.query.order_by(desc('date')).all()
	projects = Project.query.order_by(desc('date')).all()

	form = SearchBox()

	"""Placeholder for a future implementation."""
	if form.validate_on_submit():
		return redirect(url_for('main.search_result', string=form.string.data))

	return render_template('home.html',
						   title='Home',
						   form=form,
						   posts=posts,
						   projects=projects,
						   )


@main.route('/about')
def about():
	"""The 'about' page."""
	return render_template('about.html', title='About')

	# TODO: Update privacy information.


@main.route('/search')
def search_result():
	"""Placeholder for a future implementation."""

	string = request.args.get('string')
	posts = Post.query.filter_by(title=string).all()
	projects = Project.query.filter_by(title=string).all()
	users = User.query.filter_by(username=string).all()

	return render_template('search_result.html',
						   users=users,
						   posts=posts,
						   projects=projects,
						   string=string
						   )
