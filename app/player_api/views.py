from flask_restful import Resource, Api

from app import db
from app.player_api.models import Players

import json
import requests

def database_check():
    checker = Players.query.get(1)
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
            team_id = PlayersRetrieved['data'][iteration]['team_api']['id']
            team_abbreviation = PlayersRetrieved['data'][iteration]['team_api']['abbreviation']
            team_city = PlayersRetrieved['data'][iteration]['team_api']['city']
            team_conference = PlayersRetrieved['data'][iteration]['team_api']['conference']
            team_division = PlayersRetrieved['data'][iteration]['team_api']['division']
            team_full_name = PlayersRetrieved['data'][iteration]['team_api']['full_name']
            team_name = PlayersRetrieved['data'][iteration]['team_api']['name']
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
            if specific.first_name is None:
                break
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
                if specific.first_name is None:
                    break
                giving = {'first_name':specific.first_name,'last_name':specific.last_name,'position':specific.position,'height_feet':specific.height_feet,'height_inches':specific.height_inches,'weight_pounds':specific.weight_pounds,'full_name':specific.team_full_name,'name':specific.team_name}
                giving_list.append(giving)
        if giving_list != []:
            return {'data':giving_list}
        else:
            return{'error':'team_api does not exist'}

class Specific_Player(Resource):
    def get(self,first,last):
        database_check()
        dbplayers = Players.query.all()
        for specific in dbplayers:
            if specific.first_name == first and specific.last_name == last:
                return {'data':{'first_name':specific.first_name,'last_name':specific.last_name,'position':specific.position,'height_feet':specific.height_feet,'height_inches':specific.height_inches,'weight_pounds':specific.weight_pounds,'full_name':specific.team_full_name,'name':specific.team_name}}
        return {'error':'player does not exist'}
