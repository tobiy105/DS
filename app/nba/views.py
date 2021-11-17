from flask import Flask,render_template,session,request,redirect,url_for,flash,Blueprint,abort,jsonify,Response
from flask_restful import Resource, Api

from app import app, db
from app.nba.models import Team, Players
from .forms import TeamSearchForm
import json
import requests
import facebook as fb
import sys
access_token = "EAAROH8QxC4kBAMDTP87iB8fTF9eA5HEvxgpN8kX7EkAU2ZCDvGsZBvtw7VTCpmAVqZATxVPwIVaDyLopmG44WR9s4dQlqDrz2ZBcTeCFetsg3V5nlv68EyV8LEavCJzcqY0lkW2lAXh1KyHTH4WB4ZCOW8MHWToWsAkIpVrQDpXCQowsO2cC5BEQUkJfzMLj6GxGlWN9PZCIJL1yPkfepd"
app_token = "1211798249343881|KhzuT0HWz0rtTwbgbKxBFFB4uxc"
team = Blueprint('Team', __name__)

#route for team search
@app.route('/nba_post', methods=['GET','POST'])
def nba_post():
    nba_p = fb.GraphAPI(access_token)
    nba_p.put_object("me", "feed", message = "Hello welcome to my NBA Page")
    response = Response("Posted on the Facebook page", status=200)
    return response

#route for team search
@app.route('/', methods=['GET','POST'])
def team():
    form = TeamSearchForm(request.form)
    if request.method == "POST":
        team = form.team.data
        flash(f'The team is being searched', 'success')
        return redirect(url_for('retrieved', teamAsked=team))

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
            if request.method == "POST":
                team = teamAsked
                return redirect(url_for('fixtures', teamAsked=team))
            break
            return redirect(url_for('fixtures', teamAsked=teamsRetrieved))
        else:
            check += 1
    if check == 30:
        flash(f'Team does not exist')
        return redirect(url_for('team'))
    return render_template('retrieved.html',abbr=abbr,city=city,conf=conf,div=div,full=full,name=name,form=form)


@app.route('/players/<teamAsked>',methods=['GET','POST'])
def fixtures(teamAsked):
    players = requests.get('https://127.0.0.1:5000/Team_Player_List/' + teamAsked + '/')
    playersRetrieved = json.loads(players.content)
    players = playersRetrieved['data']
    return render_template('players.html',players=players)


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


# # route to update team with PUT method
# # @app.route('/teams/<int:id>', methods=['PUT'])
# class Update_Team(Resource):
#     def get(request, id):
#         '''Function to edit team in our database using team id'''
#         Team.query.get_or_404(id)
#         request_data = request.get_json()
#         Team.update_team(id=id, name=request_data["name"], full_name=request_data['full_name'],
#                       abbr=request_data['abbr'], city=request_data['city'],
#                       conf=request_data['conf'], div=request_data['div'])
#         response = Response("Team Updated", status=200, mimetype='application/json')
#         return response


# route to delete team using the DELETE method
# @app.route('/teams/<int:id>', methods=['DELETE'])
class Remove_Team(Resource):
    def get(request, id):
        '''Function to delete team from our database'''
        Team.query.get_or_404(id)
        Team.delete_team(id)
        response = Response("Team Deleted", status=200, mimetype='application/json')
        return response

def database_check():
    checker = models.Players.query.get(1)
    if checker is None:
        req = requests.get('https://www.balldontlie.io/api/v1/players')
        PlayersRetrieved = json.loads(req.content)
        iteration = 0
        while iteration < 9999:
            if PlayersRetrieved['data'][iteration]['first_name'] is None:
                break
            first_name = PlayersRetrieved['data'][iteration]['first_name']
            last_name = PlayersRetrieved['data'][iteration]['last_name']
            position = PlayersRetrieved['data'][iteration]['position']
            height_feet = PlayersRetrieved['data'][iteration]['height_feet']
            height_inches = PlayersRetrieved['data'][iteration]['height_inches']
            weight_pounds = PlayersRetrieved['data'][iteration]['weight_pounds']
            team_id = PlayersRetrieved['data'][iteration]['team']['id']
            team_abbreviation = PlayersRetrieved['data'][iteration]['team']['abbreviation']
            team_city = PlayersRetrieved['data'][iteration]['team']['city']
            team_conference = PlayersRetrieved['data'][iteration]['team']['conference']
            team_division = PlayersRetrieved['data'][iteration]['team']['division']
            team_full_name = PlayersRetrieved['data'][iteration]['team']['full_name']
            team_name = PlayersRetrieved['data'][iteration]['team']['name']
            add_player = Players(first_name=first_name,last_name=last_name,position=position,height_feet=height_feet,height_inches=height_inches,weight_pounds=weight_pounds,team_id=team_id,team_abbreviation=team_abbreviation,team_city=team_city,team_conference=team_conference,team_division=team_division,team_full_name=team_full_name,team_name=team_name)
            db.session.add(add_player)
            db.session.commit()
            iteration += 1
    return

class Full_Player_List(Resource):
    def get(self):
        database_check()
        dbplayers = Players.query.all()
        giving_list = []
        for specific in dbplayers:
            giving = {'first_name':specific.first_name,'last_name':specific.last_name,'position':specific.position,'height_feet':specific.height_feet,'height_inches':specific.height_inches,'weight_pounds':specific.weight_pounds,'full_name':specific.team_full_name,'name':specific.team_name}
            giving_list.append(giving)
        if giving_list != []:
            return {'data':giving_list}
        else:
            return{'error':'list does not exist'}

class Team_Player_List(Resource):
    def get(self,team_name):
        dbplayers = Players.query.all()
        giving_list = []
        for specific in dbplayers:
            if specific.team_name == team_name:
                giving = {'first_name':specific.first_name,'last_name':specific.last_name,'position':specific.position,'height_feet':specific.height_feet,'height_inches':specific.height_inches,'weight_pounds':specific.weight_pounds,'full_name':specific.team_full_name,'name':specific.team_name}
                giving_list.append(giving)
        if giving_list != []:
            return {'data':giving_list}
        else:
            return{'error':'team does not exist'}

class Specific_Player(Resource):
    def get(self,first,last):
        database_check()
        dbplayers = Players.query.all()
        for specific in dbplayers:
            if specific.first_name == first and specific.last_name == last:
                return {'data':{'first_name':specific.first_name,'last_name':specific.last_name,'position':specific.position,'height_feet':specific.height_feet,'height_inches':specific.height_inches,'weight_pounds':specific.weight_pounds,'full_name':specific.team_full_name,'name':specific.team_name}}
        return {'error':'player does not exist'}

