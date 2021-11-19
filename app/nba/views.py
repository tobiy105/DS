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

    playerdata = {'data':[
    {'first_name':'JAYLEN','last_name':'BROWN','number':7,'position':'G/F','height_feet':6,'height_inches':6,'weight_pounds':223,'team_name':'Celtics','team_full_name':'Boston Celtics'},
    {'first_name':'BRUNO','last_name':'FERNANDO','number':28,'position':'F/C','height_feet':6,'height_inches':9,'weight_pounds':240,'team_name':'Celtics','team_full_name':'Boston Celtics'},
    {'first_name':'SAM','last_name':'HAUSER','number':30,'position':'F','height_feet':6,'height_inches':7,'weight_pounds':217,'team_name':'Celtics','team_full_name':'Boston Celtics'},
    {'first_name':'JUANCHO','last_name':'HERNANGOMEZ','number':41,'position':'F','height_feet':6,'height_inches':9,'weight_pounds':214,'team_name':'Celtics','team_full_name':'Boston Celtics'},
    {'first_name':'AL','last_name':'HORFORD','number':42,'position':'C/F','height_feet':6,'height_inches':9,'weight_pounds':240,'team_name':'Celtics','team_full_name':'Boston Celtics'},
    {'first_name':'ENES','last_name':'KANTER','number':13,'position':'C','height_feet':6,'height_inches':10,'weight_pounds':250,'team_name':'Celtics','team_full_name':'Boston Celtics'},
    {'first_name':'ROMEO','last_name':'LANGFORD','number':9,'position':'G/F','height_feet':6,'height_inches':5,'weight_pounds':216,'team_name':'Celtics','team_full_name':'Boston Celtics'},
    {'first_name':'AARON','last_name':'NESMITH','number':26,'position':'G/F','height_feet':6,'height_inches':5,'weight_pounds':215,'team_name':'Celtics','team_full_name':'Boston Celtics'},
    {'first_name':'JABARI','last_name':'PARKER','number':20,'position':'F','height_feet':6,'height_inches':7,'weight_pounds':245,'team_name':'Celtics','team_full_name':'Boston Celtics'},
    {'first_name':'PAYTON','last_name':'PRITCHARD','number':11,'position':'G','height_feet':6,'height_inches':1,'weight_pounds':195,'team_name':'Celtics','team_full_name':'Boston Celtics'},
    {'first_name':'JOSH','last_name':'RICHARDSON','number':8,'position':'G','height_feet':6,'height_inches':5,'weight_pounds':200,'team_name':'Celtics','team_full_name':'Boston Celtics'},
    {'first_name':'DENNIS','last_name':'SCHRODER','number':71,'position':'G','height_feet':6,'height_inches':1,'weight_pounds':172,'team_name':'Celtics','team_full_name':'Boston Celtics'},
    {'first_name':'MARCUS','last_name':'SMART','number':36,'position':'G','height_feet':6,'height_inches':4,'weight_pounds':220,'team_name':'Celtics','team_full_name':'Boston Celtics'},
    {'first_name':'JAYSON','last_name':'TATUM','number':0,'position':'F/G','height_feet':6,'height_inches':8,'weight_pounds':210,'team_name':'Celtics','team_full_name':'Boston Celtics'},
    {'first_name':'BRODRIC','last_name':'THOMAS','number':97,'position':'G','height_feet':6,'height_inches':5,'weight_pounds':185,'team_name':'Celtics','team_full_name':'Boston Celtics'},
    {'first_name':'GRANT','last_name':'WILLIAMS','number':12,'position':'F','height_feet':6,'height_inches':6,'weight_pounds':236,'team_name':'Celtics','team_full_name':'Boston Celtics'},
    {'first_name':'ROBERT','last_name':'WILLIAMS III','number':44,'position':'C/F','height_feet':6,'height_inches':9,'weight_pounds':237,'team_name':'Celtics','team_full_name':'Boston Celtics'},
    {'first_name':'BOGDAN','last_name':'BOGDANOVIC','number':13,'position':'G','height_feet':6,'height_inches':6,'weight_pounds':225,'team_name':'Hawks','team_full_name':'Atlanta Hawks'},
    {'first_name':'CLINT','last_name':'CAPELA','number':15,'position':'C','height_feet':6,'height_inches':10,'weight_pounds':256,'team_name':'Hawks','team_full_name':'Atlanta Hawks'},
    {'first_name':'JOHN','last_name':'COLLINS','number':20,'position':'F/C','height_feet':6,'height_inches':9,'weight_pounds':226,'team_name':'Hawks','team_full_name':'Atlanta Hawks'},
    {'first_name':'SHARIFE','last_name':'COOPER','number':2,'position':'G','height_feet':6,'height_inches':1,'weight_pounds':176,'team_name':'Hawks','team_full_name':'Atlanta Hawks'},
    {'first_name':'GORGUI','last_name':'DIENG','number':10,'position':'C','height_feet':6,'height_inches':10,'weight_pounds':248,'team_name':'Hawks','team_full_name':'Atlanta Hawks'},
    {'first_name':'DANILO','last_name':'GALLINARI','number':8,'position':'F','height_feet':6,'height_inches':10,'weight_pounds':236,'team_name':'Hawks','team_full_name':'Atlanta Hawks'},
    {'first_name':'KEVIN','last_name':'HUERTER','number':3,'position':'G/F','height_feet':6,'height_inches':7,'weight_pounds':198,'team_name':'Hawks','team_full_name':'Atlanta Hawks'},
    {'first_name':'DEANDRE','last_name':'HUNTER','number':12,'position':'F/G','height_feet':6,'height_inches':8,'weight_pounds':221,'team_name':'Hawks','team_full_name':'Atlanta Hawks'},
    {'first_name':'SOLOMON','last_name':'HILL','number':18,'position':'F','height_feet':6,'height_inches':6,'weight_pounds':226,'team_name':'Hawks','team_full_name':'Atlanta Hawks'},
    {'first_name':'JALEN','last_name':'JOHNSON','number':1,'position':'F','height_feet':6,'height_inches':8,'weight_pounds':219,'team_name':'Hawks','team_full_name':'Atlanta Hawks'},
    {'first_name':'TIMOTHE','last_name':'LUWAWU-CABARROT','number':7,'position':'G/F','height_feet':6,'height_inches':7,'weight_pounds':215,'team_name':'Hawks','team_full_name':'Atlanta Hawks'},
    {'first_name':'SKYLAR','last_name':'MAYS','number':4,'position':'G','height_feet':6,'height_inches':4,'weight_pounds':205,'team_name':'Hawks','team_full_name':'Atlanta Hawks'},
    {'first_name':'ONYEKA','last_name':'OKONGWU','number':17,'position':'F/C','height_feet':6,'height_inches':8,'weight_pounds':240,'team_name':'Hawks','team_full_name':'Atlanta Hawks'},
    {'first_name':'CAM','last_name':'REDDISH','number':22,'position':'F/G','height_feet':6,'height_inches':8,'weight_pounds':217,'team_name':'Hawks','team_full_name':'Atlanta Hawks'},
    {'first_name':'LOU','last_name':'WILLIAMS','number':6,'position':'G','height_feet':6,'height_inches':2,'weight_pounds':175,'team_name':'Hawks','team_full_name':'Atlanta Hawks'},
    {'first_name':'DELON','last_name':'WRIGHT','number':0,'position':'G','height_feet':6,'height_inches':5,'weight_pounds':185,'team_name':'Hawks','team_full_name':'Atlanta Hawks'},
    {'first_name':'TRAE','last_name':'YOUNG','number':11,'position':'G','height_feet':6,'height_inches':1,'weight_pounds':164,'team_name':'Hawks','team_full_name':'Atlanta Hawks'},
    {'first_name':'CHARLES','last_name':'BASSEY','number':23,'position':'C/F','height_feet':6,'height_inches':9,'weight_pounds':230,'team_name':'76ers','team_full_name':'Philadelphia 76ers'},
    {'first_name':'SETH','last_name':'CURRY','number':31,'position':'G','height_feet':6,'height_inches':2,'weight_pounds':185,'team_name':'76ers','team_full_name':'Philadelphia 76ers'},
    {'first_name':'ANDRE','last_name':'DRUMMOND','number':1,'position':'C','height_feet':6,'height_inches':10,'weight_pounds':279,'team_name':'76ers','team_full_name':'Philadelphia 76ers'},
    {'first_name':'JOEL','last_name':'EMBIID','number':21,'position':'C/F','height_feet':7,'height_inches':0,'weight_pounds':280,'team_name':'76ers','team_full_name':'Philadelphia 76ers'},
    {'first_name':'DANNY','last_name':'GREEN','number':14,'position':'G','height_feet':6,'height_inches':6,'weight_pounds':215,'team_name':'76ers','team_full_name':'Philadelphia 76ers'},
    {'first_name':'TOBIAS','last_name':'HARRIS','number':12,'position':'F','height_feet':6,'height_inches':7,'weight_pounds':226,'team_name':'76ers','team_full_name':'Philadelphia 76ers'},
    {'first_name':'AARON','last_name':'HENRY','number':50,'position':'F','height_feet':6,'height_inches':5,'weight_pounds':210,'team_name':'76ers','team_full_name':'Philadelphia 76ers'},
    {'first_name':'ISAIAH','last_name':'JOE','number':7,'position':'G','height_feet':6,'height_inches':4,'weight_pounds':165,'team_name':'76ers','team_full_name':'Philadelphia 76ers'},
    {'first_name':'FURKAN','last_name':'KORKMAZ','number':30,'position':'G/F','height_feet':6,'height_inches':7,'weight_pounds':202,'team_name':'76ers','team_full_name':'Philadelphia 76ers'},
    {'first_name':'TYRESE','last_name':'MAXEY','number':0,'position':'G','height_feet':6,'height_inches':2,'weight_pounds':200,'team_name':'76ers','team_full_name':'Philadelphia 76ers'},
    {'first_name':'SHAKE','last_name':'MILTON','number':18,'position':'G/F','height_feet':6,'height_inches':5,'weight_pounds':205,'team_name':'76ers','team_full_name':'Philadelphia 76ers'},
    {'first_name':'GEORGES','last_name':'NIANG','number':20,'position':'F','height_feet':6,'height_inches':7,'weight_pounds':230,'team_name':'76ers','team_full_name':'Philadelphia 76ers'},
    {'first_name':'PAUL','last_name':'REED','number':44,'position':'F','height_feet':6,'height_inches':9,'weight_pounds':210,'team_name':'76ers','team_full_name':'Philadelphia 76ers'},
    {'first_name':'GRANT','last_name':'RILLER','number':5,'position':'G','height_feet':6,'height_inches':1,'weight_pounds':190,'team_name':'76ers','team_full_name':'Philadelphia 76ers'},
    {'first_name':'BEN','last_name':'SIMMONS','number':25,'position':'G/F','height_feet':6,'height_inches':11,'weight_pounds':240,'team_name':'76ers','team_full_name':'Philadelphia 76ers'},
    {'first_name':'JADEN','last_name':'SPRINGER','number':11,'position':'G','height_feet':6,'height_inches':4,'weight_pounds':202,'team_name':'76ers','team_full_name':'Philadelphia 76ers'},
    {'first_name':'MATISSE','last_name':'THYBULLE','number':22,'position':'G/F','height_feet':6,'height_inches':5,'weight_pounds':201,'team_name':'76ers','team_full_name':'Philadelphia 76ers'},
    {'first_name':'GRAYSON','last_name':'ALLEN','number':7,'position':'G','height_feet':6,'height_inches':4,'weight_pounds':198,'team_name':'Bucks','team_full_name':'Milwaukee Bucks'},
    {'first_name':'GIANNIS','last_name':'ANTETOKOUNMPO','number':34,'position':'F','height_feet':6,'height_inches':11,'weight_pounds':242,'team_name':'Bucks','team_full_name':'Milwaukee Bucks'},
    {'first_name':'THANASIS','last_name':'ANTETOKOUNMPO','number':43,'position':'F','height_feet':6,'height_inches':6,'weight_pounds':219,'team_name':'Bucks','team_full_name':'Milwaukee Bucks'},
    {'first_name':'PAT','last_name':'CONNAUGHTON','number':24,'position':'G','height_feet':6,'height_inches':5,'weight_pounds':209,'team_name':'Bucks','team_full_name':'Milwaukee Bucks'},
    {'first_name':'DONTE','last_name':'DIVINCENZO','number':0,'position':'G','height_feet':6,'height_inches':4,'weight_pounds':203,'team_name':'Bucks','team_full_name':'Milwaukee Bucks'},
    {'first_name':'GEORGE','last_name':'HILL','number':3,'position':'G','height_feet':6,'height_inches':4,'weight_pounds':188,'team_name':'Bucks','team_full_name':'Milwaukee Bucks'},
    {'first_name':'JRUE','last_name':'HOLIDAY','number':21,'position':'G','height_feet':6,'height_inches':3,'weight_pounds':205,'team_name':'Bucks','team_full_name':'Milwaukee Bucks'},
    {'first_name':'RODNEY','last_name':'HOOD','number':5,'position':'G/F','height_feet':6,'height_inches':8,'weight_pounds':208,'team_name':'Bucks','team_full_name':'Milwaukee Bucks'},
    {'first_name':'GEORGIOS','last_name':'KALAITZAKIS','number':18,'position':'F','height_feet':6,'height_inches':7,'weight_pounds':192,'team_name':'Bucks','team_full_name':'Milwaukee Bucks'},
    {'first_name':'BROOK','last_name':'LOPEZ','number':11,'position':'C','height_feet':7,'height_inches':0,'weight_pounds':282,'team_name':'Bucks','team_full_name':'Milwaukee Bucks'},
    {'first_name':'SANDRO','last_name':'MAMUKELASHVILI','number':54,'position':'F/C','height_feet':6,'height_inches':9,'weight_pounds':240,'team_name':'Bucks','team_full_name':'Milwaukee Bucks'},
    {'first_name':'KHRIS','last_name':'MIDDLETON','number':22,'position':'F','height_feet':6,'height_inches':7,'weight_pounds':222,'team_name':'Bucks','team_full_name':'Milwaukee Bucks'},
    {'first_name':'JORDAN','last_name':'NWORA','number':13,'position':'F','height_feet':6,'height_inches':8,'weight_pounds':225,'team_name':'Bucks','team_full_name':'Milwaukee Bucks'},
    {'first_name':'SEMI','last_name':'OJELEYE','number':37,'position':'F','height_feet':6,'height_inches':6,'weight_pounds':240,'team_name':'Bucks','team_full_name':'Milwaukee Bucks'},
    {'first_name':'BOBBY','last_name':'PORTIS','number':9,'position':'F','height_feet':6,'height_inches':10,'weight_pounds':250,'team_name':'Bucks','team_full_name':'Milwaukee Bucks'},
    {'first_name':'JUSTIN','last_name':'ROBINSON','number':55,'position':'G','height_feet':6,'height_inches':1,'weight_pounds':195,'team_name':'Bucks','team_full_name':'Milwaukee Bucks'},
    {'first_name':'LONZO','last_name':'BALL','number':2,'position':'G','height_feet':6,'height_inches':6,'weight_pounds':190,'team_name':'Bulls','team_full_name':'Chicago Bulls'},
    {'first_name':'TONY','last_name':'BRADLEY','number':13,'position':'C/F','height_feet':6,'height_inches':10,'weight_pounds':248,'team_name':'Bulls','team_full_name':'Chicago Bulls'},
    {'first_name':'TROY','last_name':'BROWN JR.','number':7,'position':'G/F','height_feet':6,'height_inches':6,'weight_pounds':215,'team_name':'Bulls','team_full_name':'Chicago Bulls'},
    {'first_name':'ALEX','last_name':'CARUSO','number':6,'position':'G','height_feet':6,'height_inches':5,'weight_pounds':186,'team_name':'Bulls','team_full_name':'Chicago Bulls'},
    {'first_name':'TYLER','last_name':'COOK','number':25,'position':'F','height_feet':6,'height_inches':8,'weight_pounds':255,'team_name':'Bulls','team_full_name':'Chicago Bulls'},
    {'first_name':'DEMAR','last_name':'DEROZAN','number':11,'position':'G/F','height_feet':6,'height_inches':6,'weight_pounds':220,'team_name':'Bulls','team_full_name':'Chicago Bulls'},
    {'first_name':'AYO','last_name':'DOSUNMU','number':12,'position':'G','height_feet':6,'height_inches':4,'weight_pounds':200,'team_name':'Bulls','team_full_name':'Chicago Bulls'},
    {'first_name':'DEVON','last_name':'DOTSON','number':3,'position':'G','height_feet':6,'height_inches':1,'weight_pounds':185,'team_name':'Bulls','team_full_name':'Chicago Bulls'},
    {'first_name':'JAVONTE','last_name':'GREEN','number':24,'position':'G/F','height_feet':6,'height_inches':5,'weight_pounds':205,'team_name':'Bulls','team_full_name':'Chicago Bulls'},
    {'first_name':'ALIZE','last_name':'JOHNSON','number':22,'position':'F','height_feet':6,'height_inches':8,'weight_pounds':212,'team_name':'Bulls','team_full_name':'Chicago Bulls'},
    {'first_name':'DERRICK','last_name':'JONES JR.','number':5,'position':'F','height_feet':6,'height_inches':6,'weight_pounds':210,'team_name':'Bulls','team_full_name':'Chicago Bulls'},
    {'first_name':'ZACK','last_name':'LAVINE','number':8,'position':'G/F','height_feet':6,'height_inches':5,'weight_pounds':200,'team_name':'Bulls','team_full_name':'Chicago Bulls'},
    {'first_name':'MARKO','last_name':'SIMONOVIC','number':19,'position':'C','height_feet':6,'height_inches':11,'weight_pounds':220,'team_name':'Bulls','team_full_name':'Chicago Bulls'},
    {'first_name':'MATT','last_name':'THOMAS','number':21,'position':'G','height_feet':6,'height_inches':3,'weight_pounds':190,'team_name':'Bulls','team_full_name':'Chicago Bulls'},
    {'first_name':'NIKOLA','last_name':'VUCEVIC','number':9,'position':'C','height_feet':6,'height_inches':10,'weight_pounds':260,'team_name':'Bulls','team_full_name':'Chicago Bulls'},
    {'first_name':'COBY','last_name':'WHITE','number':0,'position':'C/F','height_feet':6,'height_inches':4,'weight_pounds':195,'team_name':'Bulls','team_full_name':'Chicago Bulls'},
    {'first_name':'PATRICK','last_name':'WILLIAMS','number':44,'position':'F','height_feet':6,'height_inches':7,'weight_pounds':215,'team_name':'Bulls','team_full_name':'Chicago Bulls'},
    {'first_name':'KEVIN','last_name':'LOVE','number':0,'position':'F/C','height_feet':6,'height_inches':8,'weight_pounds':251,'team_name':'Cavaliers','team_full_name':'Cleveland Cavaliers'},
    {'first_name':'COLLIN','last_name':'SEXTON','number':2,'position':'G','height_feet':6,'height_inches':1,'weight_pounds':190,'team_name':'Cavaliers','team_full_name':'Cleveland Cavaliers'},
    {'first_name':'RICKY','last_name':'RUBIO','number':3,'position':'G','height_feet':6,'height_inches':2,'weight_pounds':190,'team_name':'Cavaliers','team_full_name':'Cleveland Cavaliers'},
    {'first_name':'EVAN','last_name':'MOBLEY','number':4,'position':'C','height_feet':6,'height_inches':11,'weight_pounds':215,'team_name':'Cavaliers','team_full_name':'Cleveland Cavaliers'},
    {'first_name':'RJ','last_name':'NEMBHARD JR.','number':5,'position':'G','height_feet':6,'height_inches':4,'weight_pounds':200,'team_name':'Cavaliers','team_full_name':'Cleveland Cavaliers'},
    {'first_name':'KEVIN','last_name':'PANGOS','number':6,'position':'G','height_feet':6,'height_inches':1,'weight_pounds':179,'team_name':'Cavaliers','team_full_name':'Cleveland Cavaliers'},
    {'first_name':'LAMAR','last_name':'STEVENS','number':8,'position':'F','height_feet':6,'height_inches':6,'weight_pounds':230,'team_name':'Cavaliers','team_full_name':'Cleveland Cavaliers'},
    {'first_name':'DYLAN','last_name':'WINDLER','number':9,'position':'G/F','height_feet':6,'height_inches':6,'weight_pounds':196,'team_name':'Cavaliers','team_full_name':'Cleveland Cavaliers'},
    {'first_name':'DARIUS','last_name':'GARLAND','number':10,'position':'G','height_feet':6,'height_inches':1,'weight_pounds':192,'team_name':'Cavaliers','team_full_name':'Cleveland Cavaliers'},
    {'first_name':'CEDI','last_name':'OSMAN','number':16,'position':'F','height_feet':6,'height_inches':7,'weight_pounds':230,'team_name':'Cavaliers','team_full_name':'Cleveland Cavaliers'},
    {'first_name':'ED','last_name':'DAVIS','number':21,'position':'C/F','height_feet':6,'height_inches':9,'weight_pounds':218,'team_name':'Cavaliers','team_full_name':'Cleveland Cavaliers'},
    {'first_name':'LAURI','last_name':'MARKKANEN','number':24,'position':'F/C','height_feet':6,'height_inches':11,'weight_pounds':240,'team_name':'Cavaliers','team_full_name':'Cleveland Cavaliers'},
    {'first_name':'JARRETT','last_name':'ALLEN','number':31,'position':'C','height_feet':6,'height_inches':10,'weight_pounds':243,'team_name':'Cavaliers','team_full_name':'Cleveland Cavaliers'},
    {'first_name':'DEAN','last_name':'WADE','number':32,'position':'F/C','height_feet':6,'height_inches':9,'weight_pounds':228,'team_name':'Cavaliers','team_full_name':'Cleveland Cavaliers'},
    {'first_name':'ISAAC','last_name':'OKORO','number':35,'position':'F/G','height_feet':6,'height_inches':5,'weight_pounds':225,'team_name':'Cavaliers','team_full_name':'Cleveland Cavaliers'},
    {'first_name':'DENZEL','last_name':'VALENTINE','number':45,'position':'G','height_feet':6,'height_inches':4,'weight_pounds':220,'team_name':'Cavaliers','team_full_name':'Cleveland Cavaliers'},
    {'first_name':'TACKO','last_name':'FALL','number':44,'position':'F','height_feet':6,'height_inches':7,'weight_pounds':215,'team_name':'Cavaliers','team_full_name':'Cleveland Cavaliers'},

]}
