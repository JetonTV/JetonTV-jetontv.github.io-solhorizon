# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
import pandas as pd
import csv


@blueprint.route('/index')
@login_required
def index():
    data = pd.read_csv("apps/templates/home/data.csv")
    data = data[:10]
    table = data.to_html()
    #with open("apps/templates/home/data.csv", "r") as file:
        #csv_reader = csv.reader(file)
    headers = data.columns
    table = "<table>"
    table += "<tr>"
    for header in headers:
        table += "<th>" + header + "</th>"
    table += "</tr>"
    for row in data:
        table += "<tr>"
        for cell in row:
            table += "<td>" + cell + "</td>"
        table += "</tr>"
    table += "</table>"
    print(data)
    print (table)
    return render_template('home/index.html', segment='index' , table=table)


@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:
        

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)
        data = pd.read_csv("apps/templates/home/data.csv")
        data = data[:10]
        table = data.to_html()
        with open("apps/templates/home/data.csv", "r") as file:
            csv_reader = csv.reader(file)
            headers = data.columns
            #df=pd.DataFrame(d)
            table = "<table  id='example' class='table table-striped' style='width:100%'>"
            table+="<tbody >"
            table += "<tr>"
            for header in headers:
                table += "<th scope='row'>" + header + "</th>"
            table += "</tr>"
            for row in csv_reader :
                table += "<tr>"
                for cell in row:
                    table += "<td>" + cell + "</td>"
                table += "</tr>"
            table+="</tbody>"
            table += "</table>"
        #print(data)
        #print (table)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment ,  table=table)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None




