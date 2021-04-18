from flask import Blueprint, render_template, redirect, url_for

admin = Blueprint('admin', __name__)


@admin.route('/admin', methods=['GET', 'POST'])
def admin_panel():
	"""Placeholder for future implementation"""

	return redirect(url_for('main.home'))
