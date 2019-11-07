import sys
from flask import Flask
from flask import Flask, request, session, abort, render_template, url_for, flash, redirect

from spell import app
from spell import bcrypt
from spell.spell_forms import Login, Spell, TwoFactor, Register, History
from spell.userman import Users, User, Posts, Log


import subprocess

@app.route('/')
def home():
    
    if not session.get('user'):
        return redirect(url_for('login'))
    else:
        return redirect(url_for('spell'))

@app.route('/logout')
def logout():
    if ( session.get('user') and Users.logout()) :
        flash('User successfully logged out.')
    return home()

@app.route('/login', methods=['GET','POST'])
def login():
    form = Login()
    messages = []

    if session.get('user') :
        return redirect(url_for('spell'))
    else:
        if ( "click" in request.form ) :
            if ( request.form['click'] == "Log In" ) :
                login = True
            else:
                return redirect(url_for('register'))
        else:
            login = False

        if ( login ) or ( request.method == "POST" ):
            if form.validate_on_submit():
                check = Users.check_user(form.username.data, form.password.data, form.twofapassword.data)
                if ( check[0] ):
                    if ( Users.login (form.username.data) ) :
                        messages.append('User ,' + form.username.data +", successful logged in.")
                        return render_template('spell.html', title="Spell Checker", form=Spell(), len=len(messages), messages=messages, status="result")
                else:
                    if not check[1] :
                        messages.append("Incorrect username and/or password was supplied.")

                    if not check[2] :
                        messages.append("Two-factor authentication failure was detected.")

                    return render_template('login.html', title='Login', form=form, len=len(messages), messages=messages)
            return render_template('login.html', title='Login', form=form)
                
    return render_template('login.html', title='Login', form=form)

@app.route('/register', methods=['GET','POST'])
def register():
    form=Register()
    message=""
    if session.get('user') :
        return redirect(url_for('spell'))
    else:
        if ( request.method == "POST" ) :
            if ( "click" in request.form ) and ( request.form['click'] == "Log In") :
                return redirect(url_for('login'))
            else:
                if form.validate_on_submit():
                    if ( User.query.filter_by(username=form.username.data).first() is None ) :
                        if ( Users.create_user(form.username.data, form.password.data, form.twofapassword.data) ) :
                            message = "User, " + form.username.data + ", was success fully registered."
                        else:
                            message = "User, " + form.username.data + ", was not success fully registered."
                    else:
                        message = "User, " + form.username.data + ", registration failure. User already exists."
                    
                    return render_template('register.html', title='Register', form=form, message=message)
    return render_template('register.html', title='Register', form=form)

@app.route('/spell_check', methods=['GET','POST'])
def spell():
    form = Spell()
    if not session.get('user') :
        return home()
    else :
        if ( "click" in request.form ):
            if ( request.form['click'] == "Log Out") :
                return redirect(url_for('logout'))
            else:
                if ( len (form.content.data) != 0) :
                    if sys.platform.startswith('win'):
                        result = "Windows, Testing"
                    else:
                        cmd = ["spell/bin/spell_flask", "-", "spell/bin/wordlist.txt"]
                        input = form.content.data.encode('utf-8')
                        result = subprocess.run(cmd, stdout=subprocess.PIPE, input=input).stdout.decode('utf-8')
                    
                    Users.post (form.content.data, result)

                    if result:
                        return render_template('spell.html', title='Spell Checker', form=form, message=result, input=form.content.data)
                
    return render_template('spell.html', title="Spell Checker", form=form)

@app.route('/history', methods=['GET','POST'])
def history():
    form = History()
    if not session.get('user') :
        return home()
    else :
        if (( form.username.data ) and ( session['user'] == "admin")) :
            user = form.username.data
        else :
            user = session['user']

        history = Posts.query.with_entities(Posts.id).filter_by(username=user).all()

    return render_template('history.html', Posts=history, form=form, user=user, realuser=session['user'])

@app.route("/history/query<query>")
def history_detail(query):
    if not session.get('user') :
        return home()

    history_detail = Posts.query.with_entities(Posts.id, Posts.username,Posts.spellpost, Posts.spellresult).filter_by(id=query).first()
    return render_template('history_detail.html', Post=history_detail, form=History(), realuser=session['user'])

@app.route("/login_history", methods=['GET','POST'])
def login_history():
    form = History()
    if not session.get('user') :
        return home()
    else :
        if ( session['user'] != "admin" ) :
            return home()
        else :
            if ( form.username.data ) :
                user = form.username.data
            else :
                user = session['user']

            print(user)
            log_history = Log.query.with_entities(Log.id, Log.login, Log.logout).filter_by(username=user).all()
            
            for log in log_history:
                print(log[0], log[1])

            print(log_history)
    return render_template('log_history.html', History=log_history, form=History(), user=user)
        
