from flask import (
    Blueprint, flash, g, render_template, request, url_for, session, redirect, current_app, make_response, Response, send_file
)
from app.db import get_db

import os
import time
import pandas as pd

bp = Blueprint('survey', __name__, url_prefix='/')

def to_excel(data):

    isdir = os.path.isdir('app/static/tmp/')
    if isdir == False:
        os.mkdir('app/static/tmp/')

    try:
        isFile = os.path.isfile('app/static/tmp/votes.csv')
        if isFile:
            os.remove('app/static/tmp/votes.csv')
    except:
        pass

    pd.DataFrame(data).to_csv('app/static/tmp/votes.csv')

@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@bp.route('/info', methods=['GET'])
def info():
    return render_template('info.html')

@bp.route('/data', methods=['GET'])
def data():


    db, c = get_db()
    c.execute('SELECT uuid, questions.txt as question, answers.txt as answer FROM votes INNER JOIN questions ON votes.question_id = questions.id INNER JOIN answers ON votes.answer_id = answers.id ')
    votes = c.fetchall()

    to_excel(votes)


    return send_file('static/tmp/votes.csv', as_attachment=True)
