from flask import (
    Blueprint, flash, g, render_template, request, url_for, session, redirect, current_app, make_response, send_file
)

from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import functools
import uuid
import os
import time
import datetime

from app.db import get_db
from app.ldap.global_ldap_authentication import *
from app.ldap.LoginForm import *

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # initiate the form..
        form = LoginValidation()
    
        if request.method in ('POST') :
            login_id = request.form['username']
            login_password = request.form['password']
    
            # create a directory to hold the Logs
            login_msg = global_ldap_authentication(login_id, login_password)
    
            # validate the connection
            if login_msg == "Success":
                success_message = f"*** Authentication Success "

                db, c = get_db()
                error = None
                c.execute(
                    'select id, username from users where username = %s', (login_id.lower(),)
                )

                user= c.fetchone()
                
                if user is None:
                    # insert database
                    user_uuid = str(uuid.uuid4())
                    db, c = get_db()
                    error = None
                    c.execute(
                    'insert into users (username, uuid) values (%s,%s)', (login_id.lower(),user_uuid)
                )
                                   
                    db.commit()

                    db, c = get_db()
                    c.execute(
                        'select id from users where username = %s', (login_id.lower(),)
                    )
                    id = c.fetchone()
                    session.clear()
                    session['user_id'] = id['id']
                    

                    # query questions
                    db, c = get_db()
                    error = None
                    c.execute('select id, txt from questions')
                    questions = c.fetchall()

                    # query answers
                    db, c = get_db()
                    error = None
                    c.execute('select id, question_id, txt from answers')
                    answers = c.fetchall()
                    
                    
                    resp = make_response(render_template('auth/survey.html', user_uuid=user_uuid, questions=questions, answers=answers))
                    return resp
                else:
                    session.clear()
                    session['user_id'] = user['id']
                    db, c = get_db()
                    error = None
                    c.execute(
                        'select  voted from users where username = %s', (login_id.lower(),)
                    )
                    voted = c.fetchone()
                    if voted["voted"] is None:
                        db, c = get_db()
                        error = None
                        c.execute(
                        'select  uuid from users where username = %s', (login_id.lower(),)
                    )
                        user_uuid = c.fetchone()

                        # query questions
                        db, c = get_db()
                        error = None
                        c.execute('select id, txt from questions')
                        questions = c.fetchall()

                        # query answers
                        db, c = get_db()
                        error = None
                        c.execute('select id, question_id, txt from answers')
                        answers = c.fetchall()

                        resp = make_response(render_template('auth/survey.html', user_uuid=user_uuid['uuid'], questions=questions, answers=answers))
                        return resp


                    else:
                        resp = make_response(render_template('auth/index.html'))
                        return resp
    
            else:
                error_message = f"*** Authentication Failed - {login_msg}"
                return render_template("auth/error.html", error_message=str(error_message))

        resp = make_response(render_template('auth/login.html', error=error_message))
        return resp

    else:

        resp = make_response(render_template('auth/login.html'))
        return resp


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.usert = None
    else:
        db, c = get_db()
        c.execute(
            'select * from users where id = %s', (user_id,)
        )
        g.user = c.fetchone()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

def statics():
    #get participants
    db, c = get_db()
    c.execute(
            'select participants from aux '
        )
    participants = c.fetchone()
    
    #get participation
    db, c = get_db()
    c.execute(
            'select count(distinct uuid) as participation from votes where uuid != ""'
        )
    participation = c.fetchone()
    progress = (participation['participation'] * 100)/participants['participants']

    statics_res = {'participants':participants['participants'],'participation':participation['participation'],'progress':progress }
    return statics_res

@bp.route('/')
@login_required
def index():
    resp = make_response(render_template('auth/index.html'))
    return resp

@bp.route('/vote', methods=['POST'])
@login_required
def survey():
    data = request.form
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    db, c = get_db()
    c.execute(
        'select uuid from users where id = %s', (session.get('user_id'),)
    )
    user_uuid = c.fetchone()


    for vote in data.keys():
        db, c = get_db()
        c.execute(
           'insert into votes (uuid, question_id, answer_id, timelog) values (%s,%s,%s,%s)', (user_uuid["uuid"], vote,data[vote],timestamp)
        )
        db.commit()

  

    db, c = get_db()
    c.execute(
        'update users set voted = %s where uuid like %s', (timestamp,user_uuid["uuid"])
    )
    db.commit()

    db, c = get_db()
    c.execute(
        'update users set uuid = "" where id = %s', (session.get('user_id'),)
    )
    db.commit()

    #resp = make_response(render_template('auth/index.html'))
    resp = make_response(render_template('auth/thanks.html'))
    return resp

@bp.route('/check', methods=['POST'])
@login_required
def check():
    user_uuid = request.form['uuid']

    db, c = get_db()
    c.execute(
        'SELECT questions.txt as question, answers.txt as answer FROM votes INNER JOIN questions ON votes.question_id = questions.id INNER JOIN answers ON votes.answer_id = answers.id where uuid = %s', (user_uuid,)
    )
    vote = c.fetchall()

    statics_res = statics()
  

    resp = make_response(render_template('auth/check.html', vote=vote, user_uuid=user_uuid, statics_res=statics_res))
    return resp
