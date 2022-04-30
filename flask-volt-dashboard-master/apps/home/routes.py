# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from re import U
from apps.home import blueprint
from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound


@blueprint.route('/')
def index():
    return render_template('home/index.html', segment='index')


@blueprint.route('/dashboard')
def dashboard():
    if not current_user.is_authenticated:
        return redirect(url_for('authentication_blueprint.login', form = 'login_form'))
    return render_template('home/dashboard.html', segment='dashboard')

