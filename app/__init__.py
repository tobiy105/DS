from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
api = Api(app)
from app.nba import views
from app.nba.views import Get_Teams, Get_Team_By_Id, Add_team, Add_NBA_teams, Remove_Team, Update_Team, test_add_team

api.add_resource(Get_Teams, '/get_team')
api.add_resource(Get_Team_By_Id, '/get_team_by_id/<int:id>')
api.add_resource(Add_team, '/add_team')
api.add_resource(Add_NBA_teams, '/add_nba_teams')
api.add_resource(Update_Team, '/update_team/<int:id>')
api.add_resource(Remove_Team, '/remove_team/<int:id>')
api.add_resource(test_add_team, '/test_add_team')
db.create_all()