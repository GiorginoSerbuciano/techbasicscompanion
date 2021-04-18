import base64

from flask import Blueprint, render_template, url_for
from flask.helpers import flash
from flask_login import current_user
from flask_login.utils import login_required
from requests_oauthlib import OAuth2Session
from werkzeug.utils import redirect

from tbcompanion import db
from tbcompanion.main.routes import client_id, session
from tbcompanion.models import Project, User
from tbcompanion.projects.forms import ProjectForm

projects = Blueprint('projects', __name__)


@projects.route('/project/<int:project_id>', methods=['GET'])
def project(project_id):
	"""
	This page displays an already-existing project.

	:param project_id: The ID of the project to be read from the database and presented in a HTML format.
	:return: HTML page presenting the desired project.
	"""
	g = OAuth2Session(client_id, token=session['oauth_token'])
	project_to_display = Project.query.get_or_404(project_id)
	repository = g.get(project_to_display.github_repo)

	def retrieve_readme():
		"""
		Request the README of a valid Github repository. If successful, decode the contents of the response.

		:return: String, ready for Markdown.
		:except: If no README is found, return an error message.
		"""

		try:
			request_readme = g.get(f'https://api.github.com/repos{repository.request.path_url}/contents/README.md?ref=main').json()
			readme = base64.b64decode(request_readme['content']).decode()	# base64 -> bytes -> string
			return readme
		except KeyError:
			error_text = f"Github API: 404 Not Found."
			return error_text

	def retrieve_license():
		"""
		Request the LICENSE of a valid Github repository. If successful, request the API URL of the license.
		:return: JSON-encoded contents of the response.
		:except: If no license is found, return a 'pseudo-response'.
		"""

		try:
			request_license = g.get(f'https://api.github.com/repos{repository.request.path_url}/license').json()
			request_license_json = request_license['license']
			license_json = g.get(f"https://api.github.com/licenses/{request_license_json['key']}").json()
			return license_json
		except KeyError:
			no_license = {'html_url': 'https://choosealicense.com/no-permission/', 'name': 'no license'}
			return no_license

	project_readme = retrieve_readme()
	project_license = retrieve_license()

	return render_template(
		'project_view.html',
		title=project_to_display.title,
		project=project_to_display,
		readme=project_readme,
		license=project_license)


@projects.route('/project/new', methods=['GET', 'POST'])
@login_required
def project_form():
	"""This is the page for creating a new project"""

	form = ProjectForm()
	tags = form.dropdown_tags

	if form.validate_on_submit():
		form_data_contributors = form.contributors.data.split(', ')
		project_contributors = []

		"""If the user assigns no contributors, the current user is defined as the sole contributor."""
		if form_data_contributors[0] == '':
			project_contributors.insert(0, current_user)
		else:
			for c in range(len(form_data_contributors)):
				contributor = User.query.filter_by(username=form_data_contributors[c]).first()
				project_contributors.append(contributor)
				project_contributors.insert(0, current_user)

		new_project = Project(title=form.title.data,
							  content=form.content.data,
							  admin=current_user,
							  contributors=project_contributors,  # wants User objects, not names or IDs!
							  github_repo=form.github_repo.data,
							  tag=form.tag.data
							  )

		db.session.add(new_project)
		db.session.commit()

		flash('Your project is live!', 'success')
		return redirect(url_for('main.home'))

	return render_template('project_form.html', form=form, type='project', tags=tags)
