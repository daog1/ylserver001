__author__ = 'lixiao187'

from wtforms import Form, BooleanField, TextField, PasswordField, validators,HiddenField

class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=25)])
    email = TextField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

class DeviceForm(Form):
    name = TextField('Username', [validators.Length(min=4, max=25)])
    tags = TextField('Tags', [validators.Length(min=4, max=25)])
    description = TextField('Description', [])

    '''password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')'''

class SensorForm(Form):
    name = TextField('name', [validators.Length(min=4, max=25)])
    tags = TextField('Tags', [validators.Length(min=4, max=25)])
    did = HiddenField('did',[])
    description = TextField('Description', [])
    status  = TextField('status', [])