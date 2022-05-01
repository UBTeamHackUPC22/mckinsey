# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from itertools import groupby
from re import U
from apps.home import blueprint
from flask import render_template, request, redirect, url_for, current_app, flash, g, session
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound
from flask import session

import pandas as pd
import plotly.express as px
import json
import plotly
import os

df_sales = ""
load_file_required = True

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
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], current_user.get_id(), filename)
            load_file_required = True
            file.save(file_path)

        return render_template('home/dashboard.html', 
            data=[{'name':'Days'}, {'name':'Weeks'}, {'name':'Months'}], 
            render_graphics = True,
            segment='dashboard')

    if not current_user.is_authenticated:
        return redirect(url_for('authentication_blueprint.login', form='login_form'))
    
    return render_template('home/dashboard.html', 
            data=[{'name':'Days'}, {'name':'Weeks'}, {'name':'Months'}], 
            render_graphics = False,
            segment='dashboard')

@blueprint.route('/callback', methods=['POST', 'GET'])
def callback():
    print("CALLBACK!")
    return gm(request.args.get('data'))


def gm(grouped_by = 'Days'):
    """if 'dataframe' in session:
        dict_obj = session['data']
        df_sales = pd.DataFrame(dict_obj)
    
    else:
        df_sales = pd.read_csv("..\\Data - Hack UPC\\sales.csv")
        dict_obj = df_sales.to_dict('list')
        session['dataframe'] = dict_obj"""

    global df_sales, load_file_required

    print("GM CALLED")
    if load_file_required:
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], current_user.get_id(), 'data.csv')

        if not os.path.exists(file_path):
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], '0', 'data.csv')

        df_sales = pd.read_csv(file_path)
        df_sales['date'] = pd.to_datetime(df_sales['date'])

        load_file_required = False

    print("Yeah I get to the function")
    if grouped_by == 'Days':
        fig = px.line(df_sales.groupby('date').sum()['price'])

    elif grouped_by == 'Weeks':
        df_sales['date2'] = pd.to_datetime(df_sales['date']) - pd.to_timedelta(7, unit='d')
        fig = px.line(df_sales.groupby([pd.Grouper(key='date2', freq='W-MON')])['price'].sum())

    elif grouped_by == 'Months':
        df_sales['date3'] = pd.to_datetime(df_sales['date']) - pd.to_timedelta(30, unit='d')
        fig = px.line(df_sales.groupby([pd.Grouper(key='date3', freq='1M')])['price'].sum())

    else:
        fig = px.line(df_sales.groupby('date').sum()['price'])

    print("I CALL THE CV", grouped_by)
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


@blueprint.route('/settings')
def settings():
    if not current_user.is_authenticated:
        return redirect(url_for('authentication_blueprint.login', form = 'login_form'))
    return render_template('home/settings.html', segment='dashboard')