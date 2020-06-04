import flask
from flask import Flask, render_template, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import RadioField, SelectField, SubmitField
from wtforms.validators import DataRequired
import numpy as np

from utils.draft import Draft
from utils.variables import *

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'

class DotaForm(FlaskForm):

    side = RadioField('Please choose your side:', choices=[('Radiant','Radiant'),('Dire','Dire')], validators=[DataRequired()], default='Radiant')
    radiant_hero_1 = SelectField(u'Pick First Radiant Hero:', choices=choice)
    radiant_hero_2 = SelectField(u'Pick Second Radiant Hero:', choices=choice)
    radiant_hero_3 = SelectField(u'Pick Third Radiant Hero:', choices=choice)
    radiant_hero_4 = SelectField(u'Pick Fourth Radiant Hero:', choices=choice)
    radiant_hero_5 = SelectField(u'Pick Fifth Radiant Hero:', choices=choice)
    dire_hero_1 = SelectField(u'Pick First Dire Hero:', choices=choice)
    dire_hero_2 = SelectField(u'Pick Second Dire Hero:', choices=choice)
    dire_hero_3 = SelectField(u'Pick Third Dire Hero:', choices=choice)
    dire_hero_4 = SelectField(u'Pick Fourth Dire Hero:', choices=choice)
    dire_hero_5 = SelectField(u'Pick Fifth Dire Hero:', choices=choice)
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def home():

    form = DotaForm()
    if form.validate_on_submit():
        session['side'] = form.side.data
        session['radiant_hero_1'] = form.radiant_hero_1.data
        session['radiant_hero_2'] = form.radiant_hero_2.data
        session['radiant_hero_3'] = form.radiant_hero_3.data
        session['radiant_hero_4'] = form.radiant_hero_4.data
        session['radiant_hero_5'] = form.radiant_hero_5.data
        session['dire_hero_1'] = form.dire_hero_1.data
        session['dire_hero_2'] = form.dire_hero_2.data
        session['dire_hero_3'] = form.dire_hero_3.data
        session['dire_hero_4'] = form.dire_hero_4.data
        session['dire_hero_5'] = form.dire_hero_5.data

        return redirect(url_for("solution"))

    return render_template('home.html', form=form)

@app.route('/solution')
def solution():

    if session['side']=="Radiant":
        player = 0
    else:
        player = 1

    state = [list(filter(lambda x: x!='not yet',
            [session['radiant_hero_1'],
            session['radiant_hero_2'],
            session['radiant_hero_3'],
            session['radiant_hero_4'],
            session['radiant_hero_5']])),
            list(filter(lambda x: x!='not yet',
            [session['dire_hero_1'],
            session['dire_hero_2'],
            session['dire_hero_3'],
            session['dire_hero_4'],
            session['dire_hero_5']]))]

    state =  [[int(s) for s in sublist] for sublist in state]
    # return render_template('solution.html', prediction_text='You should pick {}, {}'.format(player,state))

    avail_moves = [i for i in range(130) if i not in [0, 24, 115, 116, 117, 118, 122, 123, 124, 125, 127]]
    avail_moves = set([i for i in avail_moves if i not in state[0]+state[1]])

    d = Draft(state=state, avail_moves=avail_moves, player=player)
    p = d.get_player()
    output = p.get_move()
    hero = dict_id[output].capitalize()

    return render_template('solution.html', prediction_text='{}'.format(hero))

# if this is the main thread of execution first load the model and then start the server
if __name__ == "__main__":
    app.run(debug=True)
