from flask import Blueprint, render_template, url_for
from flask.helpers import flash
from flask_login import current_user
from flask_login.utils import login_required
from tbcompanion import db
from tbcompanion.projects.forms import ProjectForm
from tbcompanion.models import Project, User
from werkzeug.utils import redirect
import markdown

projects = Blueprint('projects', __name__)

@projects.route('/project/<int:project_id>', methods=['GET'])
def project(project_id):
	project = Project.query.get_or_404(project_id)
	return render_template('project_view.html', title=project.title, project=project)

@projects.route('/project/new', methods=['GET', 'POST'])
@login_required
def project_form():
	form = ProjectForm()
	tags = form.dropdown_tags
	if form.validate_on_submit():
		formdata_contributors = form.contributors.data.split(', ')
		project_contributors = []
		if formdata_contributors[0] == '':
			project_contributors.insert(0, current_user)
		else:
			for c in range(len(formdata_contributors)):
				contributor = User.query.filter_by(username=formdata_contributors[c]).first()
				project_contributors.append(contributor)
				project_contributors.insert(0, current_user)
		project = Project(
			title=form.title.data,
			content=form.content.data,
			admin=current_user, 
			contributors=project_contributors,	#wants User objects
			github_repo=form.github_repo.data,
			tag=form.tag.data
			)
		db.session.add(project)
		db.session.commit()
		flash('Your project is live!', 'success')
		return redirect(url_for('main.home'))
	return render_template('project_form.html', form=form, type='project', tags=tags)


