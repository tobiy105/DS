from flask import Flask, render_template, session, request, redirect, url_for, flash
from app import app
from .forms import TeamSearchForm
import json
import requests


# route for team search
@app.route('/', methods=['GET', 'POST'])
def team():
    form = TeamSearchForm(request.form)
    if request.method == "POST":
        team = form.team.data
        flash(f'The team is being searched', 'success')
        return redirect(url_for('retrieved', teamAsked=team))
    return render_template('team.html', form=form)


@app.route('/retrieved/<teamAsked>', methods=['GET', 'POST'])
def retrieved(teamAsked):
    request = requests.get('https://www.balldontlie.io/api/v1/teams')
    teamsRetrieved = json.loads(request.content)
    for finder in teamsRetrieved:
        if finder['name'] == teamsAsked:
            abbr = finder['abbreviation']
            city = finder['city']
            conf = finder['conference']
            div = finder['division']
            full = finder['full_name']
            name = finder['name']
    return render_template('retrieved.html', abbr=abbr, city=city, conf=conf, div=div, full=full, name=name)
