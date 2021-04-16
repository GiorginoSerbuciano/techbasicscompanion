import os

from flask import Blueprint, render_template, request, redirect, url_for, session
from requests_oauthlib import OAuth2Session
from sqlalchemy import desc

from tbcompanion.main.forms import SearchBox
from tbcompanion.models import Post, Project, User

main = Blueprint('main', __name__)

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
client_id = os.environ.get('TBCOMP_CLIENT_ID')
client_secret = os.environ.get('TBCOMP_CLIENT_SECRET')
authorization_base_url = 'https://github.com/login/oauth/authorize'
token_url = 'https://github.com/login/oauth/access_token'


@main.route('/github_authorization')
def github_authorization():
	g = OAuth2Session(client_id)
	authorization_url, state = g.authorization_url(authorization_base_url)
	session['oauth_state'] = state
	return redirect(authorization_url)


@main.route('/callback')
def callback():
	g = OAuth2Session(client_id,
					  state=session['oauth_state'],
					  scope=None)
	token = g.fetch_token(token_url,
						  client_secret=client_secret,
						  authorization_response=request.url)
	session['oauth_state'] = token
	return redirect(url_for('main.home'))


@main.route('/github_profile', methods=['GET'])
def profile():
	github = OAuth2Session(client_id, token=session['oauth_token'])
	return jsonify(github.get('https://api.github.com/user').json())


@main.route('/', methods=['GET', 'POST'])
def home():
	posts = Post.query.order_by(desc('date')).all()
	projects = Project.query.order_by(desc('date')).all()
	form = SearchBox()
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
	return render_template('about.html', title='About')


@main.route('/search')
def search_result():
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

# [DONE] TODO: Complete 'about'
