from flask import Flask,render_template,session,request,redirect,url_for,flash,Blueprint,abort,jsonify,Response
from flask_restful import Resource, Api
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

# route to get all teams
# @app.route('/teams', methods=['GET'])
class Get_Teams(Resource):
    def get(self):
        '''Function to get all the teams in the database'''
        return jsonify({'Teams': Team.get_all_teams()})


# route to get team by id
# @app.route('/teams/<int:id>', methods=['GET'])
class Get_Team_By_Id(Resource):
    def get(request, id):
        return_value = Team.query.get_or_404(id)

        return jsonify(return_value.name)

# route to all nba teams
# @app.route('/nba_teams', methods=['GET', 'POST'])
class Add_NBA_teams(Resource):
    def get(self):
        '''Function to add new team to our database'''
        req = requests.get('https://www.balldontlie.io/api/v1/teams')
        teamsRetrieved = json.loads(req.content)
        insert = 0
        while insert < 30:
            abbr = teamsRetrieved['data'][insert]['abbreviation']
            city = teamsRetrieved['data'][insert]['city']
            conf = teamsRetrieved['data'][insert]['conference']
            div = teamsRetrieved['data'][insert]['division']
            full = teamsRetrieved['data'][insert]['full_name']
            name = teamsRetrieved['data'][insert]['name']
            Team.add_team(name, full, abbr, city, conf, div)
            # new_team = Team(name=name, full_name=full, abbr=abbr, city=city, conf=conf, div=div)
            # db.session.add(new_team)  # add new team to database session
            # db.session.commit()  # commit changes to session
            insert += 1

        response = Response("NBA Teams added", 201, mimetype='application/json')
        return response


# route to add new team
# @app.route('/teams', methods=['POST'])
class Add_team(Resource):
    def post(self):
        '''Function to add new team to our database'''
        request_data = request.get_json()  # getting data from client
        Team.add_team(request_data["name"], request_data['full_name'],
             request_data['abbr'], request_data['city'],
             request_data['conf'], request_data['div'])
        # new_team = Team(name=request_data["name"], full_name=request_data['full_name'],
        #               abbr=request_data['abbr'], city=request_data['city'],
        #               conf=request_data['conf'], div=request_data['div'])
        # db.session.add(new_team)  # add new team to database session
        # db.session.commit()  # commit changes to session
        response = Response("Team added", 201, mimetype='application/json')
        return response

class test_add_team(Resource):
    def post(self):
        '''Function to add new team to our database'''
        request_data = request.get_json()  # getting data from client
        name = "Test"
        full = "Test_full"
        abbr = "TXT"
        city = "test_city"
        conf = "west"
        div = "north"
        new_team = Team(name=name, full_name=full, abbr=abbr, city=city, conf=conf, div=div)
        db.session.add(new_team)  # add new team to database session
        db.session.commit()  # commit changes to session
        response = Response("Team added", 201, mimetype='application/json')
        return response


# route to update team with PUT method
# @app.route('/teams/<int:id>', methods=['PUT'])
class Update_Team(Resource):
    def get(request, id):
        '''Function to edit team in our database using team id'''
        Team.query.get_or_404(id)
        request_data = request.get_json()
        Team.update_team(id=id, name=request_data["name"], full_name=request_data['full_name'],
                      abbr=request_data['abbr'], city=request_data['city'],
                      conf=request_data['conf'], div=request_data['div'])
        response = Response("Team Updated", status=200, mimetype='application/json')
        return response


# route to delete team using the DELETE method
# @app.route('/teams/<int:id>', methods=['DELETE'])
class Remove_Team(Resource):
    def get(request, id):
        '''Function to delete team from our database'''
        Team.query.get_or_404(id)
        Team.delete_team(id)
        response = Response("Team Deleted", status=200, mimetype='application/json')
        return response


