# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from re import U
from apps.home import blueprint
from flask import render_template, request, redirect, url_for, current_app, flash
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound

import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@blueprint.route('/')
def index():
    return render_template('home/index.html', segment='index')


@blueprint.route('/dashboard', methods = ('GET', 'POST'))
def dashboard():

    if request.method == 'POST':

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        # If the user does not select a file, the browser submits an
        # empty file without a filename.

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        filename = secure_filename(file.filename)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], current_user.get_id(), filename))
            return redirect(url_for('home_blueprint.dashboard'))

    if not current_user.is_authenticated:
        return redirect(url_for('authentication_blueprint.login', form = 'login_form'))
    return render_template('home/dashboard.html', segment='dashboard')


@blueprint.route('/settings')
def settings():
    if not current_user.is_authenticated:
        return redirect(url_for('authentication_blueprint.login', form = 'login_form'))
    return render_template('home/settings.html', segment='dashboard')