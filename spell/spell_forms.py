from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, InputRequired

def my_check_number(form, field):
    if ( len(field.data) > 0 and len(field.data) < 10 ):
        raise ValidationError('Phone number must be in the format xxxxxxxxxx')
    for i,c in enumerate(field.data):
        if not c.isnumeric():
            raise ValidationError('Phone number must be in the format xxxxxxxxxx')
        

class Register(FlaskForm):

    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password',validators=[InputRequired()])
#    cpassword = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password', message="Passwords must match")])
    twofapassword = StringField('9999999999', validators=[my_check_number])
#    submit = SubmitField('Register')

class Login(FlaskForm):

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    twofapassword = StringField('999-999-9999', validators=[my_check_number])
#    submit = SubmitField('Login')

class Spell(FlaskForm):
    content = TextAreaField('TYPE or PASTE your text here, then click the SPELL CHECK button', validators=[DataRequired()])
#    submit = SubmitField('Spell Check')

class TwoFactor(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
#    submit = SubmitField('Login')

class History(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])