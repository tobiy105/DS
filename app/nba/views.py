from flask import Flask,render_template,session,request,redirect,url_for,flash,Blueprint,abort,jsonify
from flask.views import MethodView
from app import app, db
from app.nba.models import Team
from .forms import TeamSearchForm
import json
import requests
import sys
team = Blueprint('Team', __name__)
#route for team search
@app.route('/', methods=['GET','POST'])
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
            return redirect(url_for('fixtures', teamAsked=teamsRetrieved))
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

class NBA_Teams(MethodView):
    def get(self, id=None, page=1):
        if not id:
            teams = Team.query.paginate(page, 10).items
            res = {}
            for team in teams:
                res[team.id] = {
                    'name': team.name,
                }
        else:
            team = Team.query.filter_by(id=id).first()
            if not team:
                abort(404)
            res = {
                'name': team.name,
            }
        return jsonify(res)

    def post(self):
        name = requests.form.get('name')
        team = Team(name)
        db.session.add(team)
        db.session.commit()
        return jsonify({team.id: {
            'name': team.name,
        }})

    def put(self, id):
        return

    def delete(self, id):
        return


team_view = NBA_Teams.as_view('team_view')
app.add_url_rule(
    '/team/', view_func=team_view, methods=['GET', 'POST']
)
app.add_url_rule(
    '/team/<int:id>', view_func=team_view, methods=['GET']
)

