from app import db

class Players(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
#    player_id = db.Column(db.Integer)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    number = db.Column(db.Integer)
    position = db.Column(db.String(255))
    height_feet = db.Column(db.Integer)
    height_inches = db.Column(db.Integer)
    weight_pounds = db.Column(db.Integer)
    team_full_name = db.Column(db.String(255))
    team_name = db.Column(db.String(255))
    

db.create_all()
