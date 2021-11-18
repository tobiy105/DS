from app import db

class Team(db.Model):
    __tablename__ = 'teams'  # creating a table name
    id = db.Column(db.Integer, primary_key=True)  # this is the primary key
    name = db.Column(db.String(80), nullable=False)
    full_name = db.Column(db.String(255), unique=True)
    abbr = db.Column(db.String(255), unique=True)
    city = db.Column(db.String(255), unique=True)
    conf = db.Column(db.String(255))
    div = db.Column(db.String(255))


    def json(self):
        return {'id': self.id, 'name': self.name,
                'full_name': self.full_name, 'abbr': self.abbr, 'city': self.city,
                'conf': self.conf, 'div': self.div}
        # this method we are defining will convert our output to json


    def add_team(_name, _full_name, _abbr, _city, _conf, _div):
        '''function to add team to database using _title, _year, _genre
        as parameters'''
        # creating an instance of our Team constructor
        new_team = Team(name=_name, full_name=_full_name, abbr=_abbr, city=_city, conf=_conf, div=_div)
        db.session.add(new_team)  # add new team_api to database session
        db.session.commit()  # commit changes to session

    def get_all_teams():
        '''function to get all teams in our database'''
        return [Team.json(team) for team in Team.query.all()]

    def get_team(_id):
        '''function to get team_api using the id of the team_api as parameter'''
        return [Team.json(Team.query.filter_by(id=_id).first())]
        # Team.json() coverts our output to json
        # the filter_by method filters the query by the id
        # the .first() method displays the first value


    def delete_team(_id):
        '''function to delete a team_api from our database using
           the id of the team_api as a parameter'''
        Team.query.filter_by(id=_id).delete()
        # filter by id and delete
        db.session.commit()  # commiting the new change to our database


db.create_all()