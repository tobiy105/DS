from flask import Flask,render_template,session,request,redirect,url_for,flash,Blueprint,abort,jsonify,Response

from app import app, db
from app.team_api.views import Get_Teams
from .forms import TeamSearchForm, SearchForm
import json
import requests
import facebook as fb
import sys
access_token = "EAAROH8QxC4kBAMDTP87iB8fTF9eA5HEvxgpN8kX7EkAU2ZCDvGsZBvtw7VTCpmAVqZATxVPwIVaDyLopmG44WR9s4dQlqDrz2ZBcTeCFetsg3V5nlv68EyV8LEavCJzcqY0lkW2lAXh1KyHTH4WB4ZCOW8MHWToWsAkIpVrQDpXCQowsO2cC5BEQUkJfzMLj6GxGlWN9PZCIJL1yPkfepd"
app_token = "1211798249343881|KhzuT0HWz0rtTwbgbKxBFFB4uxc"
team = Blueprint('Team', __name__)

# using graph api to post a message
@app.route('/nba_post/<post>', methods=['GET','POST'])
def nba_post(post):
    nba_p = fb.GraphAPI(access_token)
    nba_p.put_object("me", "feed", message = post)
    response = Response("Posted on the Facebook page", status=200)
    return response

#route for team_api search
# takes an team name from client
@app.route('/', methods=['GET','POST'])
def team():
    form = TeamSearchForm(request.form)
    if request.method == "POST":
        team = form.team.data
        flash(f'The team_api is being searched', 'success')
        return redirect(url_for('retrieved', teamAsked=team))

    return render_template('team.html', form=form)

#
@app.route('/retrieved/<teamAsked>',methods=['GET','POST'])
def retrieved(teamAsked):
    # I think we add a for loop to get a id for team_api
    req = requests.get('https://127.0.0.1:5000/get_team')
    teamsRetrieved = json.loads(req.content)
    form = SearchForm(request.form)
    form.fixture.data = teamAsked
    check = 0
    while check < 30:
        if teamsRetrieved['Teams'][check]['name'] == teamAsked:
            abbr = teamsRetrieved['Teams'][check]['abbr']
            city = teamsRetrieved['Teams'][check]['city']
            conf = teamsRetrieved['Teams'][check]['conf']
            div = teamsRetrieved['Teams'][check]['div']
            full = teamsRetrieved['Teams'][check]['full_name']
            name = teamsRetrieved['Teams'][check]['name']
            if request.method == "POST":
                team = teamAsked
                return redirect(url_for('players', teamAsked=team))
            break
        else:
            check += 1
    if check == 30:
        flash(f'Team does not exist')
        return redirect(url_for('team'))
    return render_template('retrieved.html', abbr=abbr, city=city, conf=conf, div=div, full=full, name=name, form=form)


@app.route('/players/<teamAsked>',methods=['GET','POST'])
def fixtures(teamAsked):
    players = requests.get('https://127.0.0.1:5000/Team_Player_List/' + teamAsked + '/')
    playersRetrieved = json.loads(players.content)
    players = playersRetrieved['data']
    return render_template('players.html',players=players)
