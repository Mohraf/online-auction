from unicodedata import category
from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,ValidationError, SelectField, TextField
from wtforms.validators import Required,Email
from ..models import User


class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')


class ItemForm(FlaskForm):
    name = StringField('Enter Item Name.',validators = [Required()])
    description = TextAreaField('Enter Description Of The Item.')
    startingPrice = StringField('Enter Your Starting Price.')
    submit = SubmitField('Submit')