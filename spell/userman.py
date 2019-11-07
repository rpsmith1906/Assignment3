#!/usr/bin/python3
import os.path

from flask import Flask, session
from spell import bcrypt
from spell import db
from datetime import datetime, date, time

class User(db.Model):
    #id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), primary_key=True, unique=True, nullable=False)
    password = db.Column(db.String(60), unique=True, nullable=False)
    twofapassword = db.Column(db.String(10))
    sessions = db.relationship('Log', backref='user', lazy=True)
    posts = db.relationship('Posts', backref='user', lazy=True)

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.DateTime)
    logout = db.Column(db.DateTime)
    username = db.Column(db.String(20), db.ForeignKey('user.username'), nullable=False)
    posts = db.relationship('Posts', backref='log', lazy=True)

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spellpost = db.Column(db.String(100000))
    spellresult = db.Column(db.String(40000))
    username = db.Column(db.String(20), db.ForeignKey('user.username'), nullable=False)
    session = db.Column(db.Integer, db.ForeignKey('log.id'), nullable=False)

class Users():
    #password = {}
    #twofapassword = {}

    def create_user(username, password, twofapassword):
        row = User()
        row.username = username
        row.password = bcrypt.generate_password_hash(password).decode('utf-8')
        if ( len(twofapassword) > 0 ) :
            row.twofapassword = twofapassword
        
        try:
            db.session.add(row)
            db.session.commit()
            return ( True )
        except:
            db.session.rollback() 
            return( False )

    def check_user(username, password, twofapassword) :
        if ( User.query.filter_by(username=username).first() is None ) :
            return ( False, False, False )
        else:
            pw = User.query.filter_by(username=username).first().password
            if ( not bcrypt.check_password_hash(pw, password) ) :
                passw = False
            else:
                passw = True

            pw = User.query.filter_by(username=username).first().twofapassword
            if ( pw is None ) :
                if ( len( twofapassword ) != 0 ) :
                    twofa = False
                else:
                    twofa = True
            else:
                if ( pw == twofapassword ) :
                    twofa = True
                else:
                    twofa = False
        return ( passw and twofa, passw, twofa )

    def login( username ) :
        row = Log()
        row.username = username
        row.login = datetime.now()
        session['user'] = username
        
        try:
            db.session.add(row)
            db.session.commit()
            session['session_id'] = row.id
            return ( True )
        except:
            db.session.rollback() 
            return( False )

    def logout() :
        row = Log()
        row = Log.query.filter_by(id=session['session_id']).first()

        if ( row is None ) :
            session.pop('user')
            return ( True )

        row.logout = datetime.now()
        
        try:
            db.session.commit()
            session.pop('user')
            return ( True )
        except:
            db.session.rollback() 
            return( False )

    def post(spellpost, spellresult) :
        row = Posts()
        row.spellpost = spellpost
        row.spellresult = spellresult
        row.session = session['session_id']
        row.username = session['user']

        try:
            db.session.add(row)
            db.session.commit()
            return ( True )
        except:
            db.session.rollback() 
            return( False )
