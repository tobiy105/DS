from flask import Flask,render_template,session,request,redirect,url_for,flash,Blueprint,abort,jsonify,Response
from flask_restful import Resource, Api

from app import app, db
from app.team_api.models import Team

import json
import requests


# route to get all teams
# @app.route('/teams', methods=['GET'])
class Get_Teams(Resource):
    def get(self):
        '''Function to get all the teams in the database'''
        return jsonify({'Teams': Team.get_all_teams()})


# route to get team_api by id
# @app.route('/teams/<int:id>', methods=['GET'])
class Get_Team_By_Id(Resource):
    def get(request, id):
        return_value = Team.query.get_or_404(id)

        return jsonify(return_value.name)

# route to all nba teams
# @app.route('/nba_teams', methods=['GET', 'POST'])
class Add_NBA_teams(Resource):
    def get(self):
        '''Function to add new team_api to our database'''
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
            # db.session.add(new_team)  # add new team_api to database session
            # db.session.commit()  # commit changes to session
            insert += 1

        response = Response("NBA Teams added", 201, mimetype='application/json')
        return response


# route to add new team_api
# @app.route('/teams', methods=['POST'])
class Add_team(Resource):
    def post(self):
        '''Function to add new team_api to our database'''
        request_data = request.get_json()  # getting data from client
        Team.add_team(request_data["name"], request_data['full_name'],
             request_data['abbr'], request_data['city'],
             request_data['conf'], request_data['div'])
        # new_team = Team(name=request_data["name"], full_name=request_data['full_name'],
        #               abbr=request_data['abbr'], city=request_data['city'],
        #               conf=request_data['conf'], div=request_data['div'])
        # db.session.add(new_team)  # add new team_api to database session
        # db.session.commit()  # commit changes to session
        response = Response("Team added", 201, mimetype='application/json')
        return response


# route to delete team_api using the DELETE method
# @app.route('/teams/<int:id>', methods=['DELETE'])
class Remove_Team(Resource):
    def get(request, id):
        '''Function to delete team_api from our database'''
        Team.query.get_or_404(id)
        Team.delete_team(id)
        response = Response("Team Deleted", status=200, mimetype='application/json')
        return response

