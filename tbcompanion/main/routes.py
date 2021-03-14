from flask import Blueprint, render_template, request
from flask.helpers import url_for
from sqlalchemy import desc
from tbcompanion.main.forms import SearchBox
from tbcompanion.models import Post, Project, User
from werkzeug.utils import redirect

main = Blueprint('main', __name__)

@main.route('/', methods=['GET','POST'])
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
