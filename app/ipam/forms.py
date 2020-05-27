from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, NumberRange
from flask import render_template, current_app

from app.model import User


class RequestIpForm(FlaskForm):
    fqdn = StringField('FQDN (e.g. srv000000.mud.internal.co.za)', validators=[DataRequired()])
    network = SelectField('Subnet', validators=[DataRequired()],
        choices=[('10.84.0.0','DEV - 10.84.0.0'),('10.83.0.0','PRD - 10.83.0.0')])
    ipcount = IntegerField('IPs Required (max 10)', [NumberRange(min=1, max=10)],default='1')
    submit = SubmitField('Request IPs')




