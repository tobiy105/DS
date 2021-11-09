from flask import render_template,session, request,redirect,url_for,flash
from app import app
from .forms import TeamSearchForm

#route for team search
@app.route('/', methods=['GET','POST'])
def team():
    form = TeamSearchForm(request.form)
    if request.method == "POST":
        team = form.team.data
        flash(f'The team is being searched', 'success')
        print(team)

    return render_template('team.html', form=form)
