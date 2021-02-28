from flask import Blueprint, render_template, url_for
from flask.helpers import flash
from flask_login import current_user
from flask_login.utils import login_required
from tbcompanion import db
from tbcompanion.projects.forms import ProjectForm
from tbcompanion.models import Project, Tag
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
	tags = Tag.query.order_by(Tag.id).all()
	if form.validate_on_submit():
		project = Project(
			title=form.title.data,
			content=form.content.data,
			contributor=current_user,
			github_repo=form.github_repo.data)
		db.session.add(project)
		db.session.commit()
		flash('Your project is live!', 'success')
		return redirect(url_for('main.home'))
	return render_template('project_form.html', form=form, type='project', tags=tags)


