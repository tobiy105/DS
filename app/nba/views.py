from flask import Flask,render_template,session, request,redirect,url_for,flash
from app import app
from .forms import TeamSearchForm
import json
import requests
import sys

#route for team search
@app.route('/team', methods=['GET','POST'])
def team():
    form = TeamSearchForm(request.form)
    if request.method == "POST":
        team = form.team.data
        flash(f'The team is being searched', 'success')
        return redirect(url_for('retrieved', teamAsked=team))
    fix = requests.get('https://www.balldontlie.io/api/v1/games')
    fixturesRetrieved = json.loads(fix.content)
    check = 0
    amount = 0
    return render_template('team.html', form=form)
    
@app.route('/retrieved/<teamAsked>',methods=['GET','POST'])
def retrieved(teamAsked):
    req = requests.get('https://www.balldontlie.io/api/v1/teams')
    teamsRetrieved = json.loads(req.content)
    check = 0
    while check < 30:
        if teamsRetrieved['data'][check]['name'] == teamAsked:
            abbr = teamsRetrieved['data'][check]['abbreviation']
            city = teamsRetrieved['data'][check]['city']
            conf = teamsRetrieved['data'][check]['conference']
            div = teamsRetrieved['data'][check]['division']
            full = teamsRetrieved['data'][check]['full_name']
            name = teamsRetrieved['data'][check]['name']
            break
        else:
            check += 1
    return render_template('retrieved.html',abbr=abbr,city=city,conf=conf,div=div,full=full,name=name)

@app.route('/fixtures/<teamAsked>',methods=['GET','POST'])
def fixtures(teamAsked):
    fix = requests.get('https://www.balldontlie.io/api/v1/games')
    fixturesRetrieved = json.loads(fix.content)
    incr = 0
    amount = 0
    games = []
    while incr < 25:
        if fixturesRetrieved['data'][incr]['home_team']['name'] == teamAsked:
            games.append(fixturesRetrieved['data'][incr]['home_team']['name'])
            games.append(fixturesRetrieved['data'][incr]['visitor_team']['name'])
            games.append(fixturesRetrieved['data'][incr]['date'])
            games.append(fixturesRetrieved['data'][incr]['home_team_score'])
            games.append(fixturesRetrieved['data'][incr]['visitor_team_score'])
            if fixturesRetrieved['data'][incr]['home_team_score'] < fixturesRetrieved['data'][incr]['visitor_team_score']:
                games.append(fixturesRetrieved['data'][incr]['visitor_team']['name'])
            else:
                games.append(fixturesRetrieved['data'][incr]['home_team']['name'])
            incr += 1
            amount += 1
        elif fixturesRetrieved['data'][incr]['visitor_team']['name'] == teamAsked:
            games.append(fixturesRetrieved['data'][incr]['home_team']['name'])
            games.append(fixturesRetrieved['data'][incr]['visitor_team']['name'])
            games.append(fixturesRetrieved['data'][incr]['date'])
            games.append(fixturesRetrieved['data'][incr]['home_team_score'])
            games.append(fixturesRetrieved['data'][incr]['visitor_team_score'])
            if fixturesRetrieved['data'][incr]['home_team_score'] < fixturesRetrieved['data'][incr]['visitor_team_score']:
                games.append('Winning Team: ' + fixturesRetrieved['data'][incr]['visitor_team']['name'])
            else:
                games.append('Winning Team: ' + fixturesRetrieved['data'][incr]['home_team']['name'])
            incr += 1
            amount += 1
        else:
            incr += 1
    return render_template('fixtures.html',games=games,amount=amount)
