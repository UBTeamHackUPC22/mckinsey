# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from itertools import groupby
from re import U
from apps.home import blueprint
from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound
from flask import session

import pandas as pd
import plotly.express as px
import json
import plotly

import os

df_sales = ""
first_time = True


@blueprint.route('/')
def index():
    return render_template('home/index.html', segment='index')


@blueprint.route('/dashboard')
def dashboard():
    if not current_user.is_authenticated:
        return redirect(url_for('authentication_blueprint.login', form='login_form'))
    
    return render_template('home/dashboard.html', data=[{'name':'Days'}, {'name':'Weeks'}, {'name':'Months'}], segment='dashboard')

@blueprint.route('/callback', methods=['POST', 'GET'])
def callback():
    return gm(request.args.get('data'))


def gm(grouped_by='Days'):

    """if 'dataframe' in session:
        dict_obj = session['data']
        df_sales = pd.DataFrame(dict_obj)
    
    else:
        df_sales = pd.read_csv("..\\Data - Hack UPC\\sales.csv")
        dict_obj = df_sales.to_dict('list')
        session['dataframe'] = dict_obj"""

    global df_sales, first_time
    if first_time:
        first_time = False
        df_sales = pd.read_csv("..\\Data - Hack UPC\\sales.csv")
        df_sales['date'] = pd.to_datetime(df_sales['date'])

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
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
