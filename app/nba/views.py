<<<<<<< HEAD
from flask import Flask, render_template, session, request, redirect, url_for, flash
from app import app
from .forms import TeamSearchForm
import json
import requests


# route for team search
@app.route('/', methods=['GET', 'POST'])
=======
from flask import Flask,render_template,session, request,redirect,url_for,flash
from app import app
from .forms import TeamSearchForm
import json

#route for team search
@app.route('/team', methods=['GET','POST'])
>>>>>>> bdd3c24bb88b80228e6b7f7fef5eb0e81d0d94a3
def team():
    form = TeamSearchForm(request.form)
    if request.method == "POST":
        team = form.team.data
        flash(f'The team is being searched', 'success')
<<<<<<< HEAD
        return redirect(url_for('retrieved', teamAsked=team))
    return render_template('team.html', form=form)


@app.route('/retrieved/<teamAsked>', methods=['GET', 'POST'])
=======
        return redirect(url_for('retrieved',teamAsked=team))
    return render_template('team.html', form=form)
    
@app.route('/retrieved/<teamAsked>',methods=['GET','POST'])
>>>>>>> bdd3c24bb88b80228e6b7f7fef5eb0e81d0d94a3
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
<<<<<<< HEAD
    return render_template('retrieved.html', abbr=abbr, city=city, conf=conf, div=div, full=full, name=name)
=======
    return render_template('retrieved.html',abbr=abbr,city=city,conf=conf,div=div,full=full,name=name)
>>>>>>> bdd3c24bb88b80228e6b7f7fef5eb0e81d0d94a3
