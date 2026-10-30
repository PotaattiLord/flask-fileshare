from flask import render_template, flash, redirect, url_for
from app import app, db
from app.errors import bp

@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500

@bp.app_errorhandler(403)
def forbidden_error(error):
    return render_template('errors/403.html'), 403

@bp.app_errorhandler(405)
def method_not_allowed_error(error):
    return render_template('errors/405.html'), 405

@bp.app_errorhandler(413)
def request_entity_too_large(error):
    flash('File is too large. Maximum file size is {} MB.'.format(app.config['MAX_CONTENT_LENGTH'] / 1048576), 'danger')
    return redirect(url_for('auth.index'))
