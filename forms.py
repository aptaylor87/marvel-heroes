from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Length


class CharacterSearchForm(FlaskForm):
    """Character Search Form"""

    hero_one = TextAreaField('Hero One', validators=[DataRequired()])
    hero_two = TextAreaField('Hero Two', validators=[DataRequired()])

class UserForm(FlaskForm):
    """Form for adding users and logging in users"""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6), DataRequired()])
    
