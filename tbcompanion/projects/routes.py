from flask import Blueprint, render_template, url_for
from flask.helpers import flash
from flask_login import current_user
from flask_login.utils import login_required
from tbcompanion import db
from tbcompanion.projects.forms import ProjectForm
from tbcompanion.models import Project, User
from werkzeug.utils import redirect

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
		project = Project(
			title=form.title.data,
			content=form.content.data,
			admin=current_user, 
			#ISSUE: #10 AttributeError: 'str' object has no attribute '_sa_instance_state'
			github_repo=form.github_repo.data,
			tag=form.tag.data
			)
		contributors_list = form.contributors.data.split(', ')
		for c in contributors_list:
			contributor = User.query.filter_by(username=c).first()
			project.contributor_id.append(contributor)
		db.session.add(project)
		db.session.commit()
		flash('Your project is live!', 'success')
		return redirect(url_for('main.home'))
	return render_template('project_form.html', form=form, type='project', tags=tags)


