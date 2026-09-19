from flask import render_template, flash, redirect, url_for, request, abort, send_from_directory
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
import os
import sqlalchemy as sa
from app import app, db
from app.auth.forms import LoginForm, RegistrationForm, UploadForm
from app.auth import bp
from app.models import User, File
from flask_babel import _

@bp.route('/')
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    private_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'private', str(current_user.id))
    public_user_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'public', str(current_user.id))

    if not os.path.exists(private_folder):
        os.makedirs(private_folder)
    if not os.path.exists(public_user_folder):
        os.makedirs(public_user_folder)

    files = os.listdir(private_folder)
    public_files = []
    public_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'public')
    for (root, dirs, filenames) in os.walk(public_folder):
        for filename in filenames:
            relative_path = os.path.relpath(os.path.join(root, filename), public_folder)
            file_name = os.path.basename(relative_path)
            owner_id = int(relative_path.split(os.sep, 1)[0])
            owner = db.session.get(User, owner_id)
            public_files.append({'path': relative_path, 'name': file_name, 'owner': owner})
    
    if request.method == 'POST':
        form = UploadForm()
        if form.validate_on_submit():
            uploaded_file = request.files['file']
            if uploaded_file.filename != '':
                filename = secure_filename(uploaded_file.filename)
                if form.is_public.data:
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'public', str(current_user.id), filename)
                    if not os.path.exists(os.path.dirname(file_path)):
                        os.makedirs(os.path.dirname(file_path))
                else:
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'private', str(current_user.id), filename)
                    if not os.path.exists(os.path.dirname(file_path)):
                        os.makedirs(os.path.dirname(file_path))
                uploaded_file.save(file_path)
                flash(_('File successfully uploaded'))
                return redirect(url_for('index'))
            else:
                flash(_('No selected file'))
                return redirect(request.url)
    upload_form = UploadForm()

    return render_template('index.html', title='Home', user=current_user, user_id=current_user.id, files=files, public_files=public_files, upload_form=upload_form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash(_('Invalid username or password'))
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('auth.index'))
    return render_template('auth/login.html', title='Sign In', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(_('Congratulations, you are now a registered user!'))
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.index'))

@bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        form = UploadForm()
        if form.validate_on_submit():
            uploaded_file = request.files['file']
            if uploaded_file.filename != '':
                filename = secure_filename(uploaded_file.filename)
                if form.is_public.data:
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'public', str(current_user.id), filename)
                    if not os.path.exists(os.path.dirname(file_path)):
                        os.makedirs(os.path.dirname(file_path))
                else:
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'private', str(current_user.id), filename)
                    if not os.path.exists(os.path.dirname(file_path)):
                        os.makedirs(os.path.dirname(file_path))
                uploaded_file.save(file_path)
                flash(_('File successfully uploaded'))
                return redirect(url_for('index'))
            else:
                flash(_('No selected file'))
                return redirect(request.url)
    form = UploadForm()
    return render_template('upload.html', title='Upload File', form=form)

@bp.route("/uploads/public/<path:filename>")
@login_required
def public_file(filename):
    public_root = os.path.join(app.config["UPLOAD_FOLDER"], "public")
    return send_from_directory(public_root, filename)


@bp.route('/uploads/private/<int:user_id>/<path:filename>')
@login_required
def private_file(user_id, filename):
    if user_id != current_user.id:
        abort(403)

    private_root = os.path.join(app.config['UPLOAD_FOLDER'], 'private', str(user_id))
    return send_from_directory(private_root, filename)

@bp.route('/delete/<string:access>/<int:user_id>/<path:filename>', methods=['POST'])
@login_required
def delete_file(user_id, filename, access):
    if user_id != current_user.id:
        abort(403)

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], access, str(user_id), filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        flash(_('File successfully deleted'))
    else:
        flash(_('File not found'))
    return redirect(url_for('auth.index'))