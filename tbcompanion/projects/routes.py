from flask import Blueprint, render_template, url_for
from flask.helpers import flash
from flask_login import current_user
from flask_login.utils import login_required
from requests_oauthlib import OAuth2Session
from werkzeug.utils import redirect

from tbcompanion import db
from tbcompanion.main.routes import client_id
from tbcompanion.models import Project, User
from tbcompanion.projects.forms import ProjectForm

import base64

projects = Blueprint('projects', __name__)


@projects.route('/project/<int:project_id>', methods=['GET'])
def project(project_id):
	"""
	This page displays an already-existing project.

	:param project_id:
	:return:
	"""
	g = OAuth2Session(client_id)
	project_to_display = Project.query.get_or_404(project_id)

	def retrieve_readme(query_repo):
		"""
		If a valid Github repository is assigned to the project displayed, this function will retrieve its README.

		:param query_repo: The repository assigned to the project displayed, equal to project_to_display.github_repo.
		:return: (try) Markdown-compatible text {str}; (except) Error text replacing README text {str}.
		"""
		repository = query_repo.github_repo[19:]	# removes 'https://github.com'
		try:
			request = g.get(f'https://api.github.com/repos/{repository}/readme').json()
			readme = base64.b64decode(request['content']).decode()	# base64 -> bytes -> string
			return readme
		except KeyError:	# raised by readme when request returns <Response[404]>
			error_text = f"Github API: {request['message']}. Couldn't find a README in repository {repository}."
			return error_text

	project_readme = retrieve_readme(project_to_display)

	return render_template(
		'project_view.html',
		title=project_to_display.title,
		project=project_to_display,
		readme=project_readme)


@projects.route('/project/new', methods=['GET', 'POST'])
@login_required
def project_form():
	form = ProjectForm()
	tags = form.dropdown_tags
	if form.validate_on_submit():
		form_data_contributors = form.contributors.data.split(', ')
		project_contributors = []
		if form_data_contributors[0] == '':
			project_contributors.insert(0, current_user)
		else:
			for c in range(len(form_data_contributors)):
				contributor = User.query.filter_by(username=form_data_contributors[c]).first()
				project_contributors.append(contributor)
				project_contributors.insert(0, current_user)
		project = Project(
			title=form.title.data,
			content=form.content.data,
			admin=current_user,
			contributors=project_contributors,  # wants User objects
			github_repo=form.github_repo.data,
			tag=form.tag.data
		)
		db.session.add(project)
		db.session.commit()
		flash('Your project is live!', 'success')
		return redirect(url_for('main.home'))
	return render_template('project_form.html', form=form, type='project', tags=tags)
