import os

from flask import Flask, request, render_template, redirect, flash, session, g, jsonify

# from flask_debugtoolbar import DebugToolbarExtension

from forms import CharacterSearchForm, UserForm
from models import db, connect_db, Character, User, Comic, Reading_List
from marvel import *

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///marvel_app_db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = "un7FzLX5iidp7d"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# debug = DebugToolbarExtension(app)

error_message = "Something went wrong"

connect_db(app)


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/')
def home_page():
    """redirects to search, which serves as the home page"""
    return redirect('/search')


@app.route('/register', methods = ['GET', 'POST'])
def register_user():
    """Displays a user registration form, and then creates the user when form is submitted"""
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        new_user = User.register(username, password)
        try:
            db.session.commit()
            do_login(new_user)
            flash('Welcome!')
            return redirect('/search')
        except:
            flash(error_message)
            db.session.rollback()
            return redirect('/register')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    """Displays a form for a user to log in, then handles login when the form is submitted"""
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)

        if user:
            flash(f'Welcome Back, {user.username}')
            do_login(user)
            return redirect('/search')
        else:
            flash('Invalid username/password.')

    return render_template('login.html', form=form)

@app.route('/logout')  
def logout_user():
    """Logs the user out"""
    do_logout()
    flash('Goodbye!')
    return redirect('/search')



@app.route('/search', methods =['GET', 'POST'])
def search():
    """This page renders the search form, or it renders the first page of search results if they've been submitted. This route calls the Marvel API to a specific route that will return a list of comics that feature both of the characters included in the request. 
    
    None of the comics in the results are stored in the database at this stage, they are only added to the database if they are added to a user's reading list. 
    """
    form = CharacterSearchForm()

    if form.validate_on_submit():
        
        character_one = form.hero_one.data
        character_two = form.hero_two.data
       
        try:
            character_one_db = Character.query.filter_by(name=character_one).first()
            character_two_db = Character.query.filter_by(name=character_two).first()
            
            search = get_shared_appearances(character_one_db.id, character_two_db.id)
            comics = search[0]
            total_results = search[1]

            if g.user:
                user  = User.query.get_or_404(g.user.id)
                user_comics = user.get_list_of_added_comics()
            else:
                user_comics = []
        
            return render_template('/show_comics.html', comics = comics, character_one=character_one_db, character_two=character_two_db, total_results=total_results, offset=0, user_comics=user_comics)
        
        except:
            flash(error_message)
            db.session.rollback()
            return redirect('/search')

    else:

        return render_template('search_character_form.html', form=form)

@app.route('/search_results/<int:char_one>/<int:char_two>/<int:offset>/<int:total>')
def show_more_search_results(char_one, char_two, offset, total):
    """This is a companion route to '/search.' It handles the pagination of results by working with the offset parameter from the API and returns a list of comics featuring both searched characters"""

    try:
        character_one_db = Character.query.get(char_one)
        character_two_db = Character.query.get(char_two)

        search = get_shared_appearances(character_one_db.id, character_two_db.id, offset)
        comics = search[0]

        if g.user:
                user  = User.query.get_or_404(g.user.id)
                user_comics = user.get_list_of_added_comics()
        else:
            user_comics = []
            
        return render_template('/show_comics.html', comics = comics, character_one=character_one_db, character_two=character_two_db, total_results=total, offset=offset, user_comics=user_comics)
    
    except:
        flash(error_message)
        db.session.rollback()
        return redirect('/search')

@app.route('/reading_list')
def show_reading_list():
    """This route directs to a page showing a user the comics they have added to their reading list. If a user is not logged in the are redirected back to search with a flashed message"""

    if  not g.user:
        flash('Log in or create an account to make a reading list.')
        return redirect('/search')

    user  = User.query.get_or_404(g.user.id)
    comics = user.comics
    return render_template('reading_list.html', comics=comics)




@app.route('/api/addreadinglist', methods=['POST'])
def create_readinglist_item():
    """This is an API route that is used in main.js. It takes in a comic id and user id. First a check is run to see if a comic with this id is in the comics table, and if not, it creates one. Then the comic id and user id are used to create a reading list item. """
    user_id = request.json['user_id']
    comic_id = request.json['comic_id']
    
    character_one = request.json['character_one']
    character_two  = request.json['character_two']


    if Comic.query.filter(Comic.id == comic_id).count():

        reading_list = Reading_List(user_id=user_id, comic_id=comic_id, character_one_name=character_one, character_two_name=character_two)
        db.session.add(reading_list)
        db.session.commit()
    else:
        new_comic = get_comic(comic_id)
        print(new_comic)
        db.session.add(new_comic)
        db.session.commit()

        reading_list = Reading_List(user_id=user_id, comic_id=comic_id, character_one_name=character_one, character_two_name=character_two)
        print(reading_list)
        db.session.add(reading_list)
        db.session.commit()



    return jsonify(reading_list=reading_list.serialize_reading_list())

@app.route('/api/deletereadinglist', methods=['POST'])
def delete_readinglist_item():
    """This is an API route that is used in main.js. It takes a user ID and comic id and removes the relevant entry from the reading_list table"""

    user_id = request.json['user_id']
    comic_id = request.json['comic_id']
    reading_list_comic = Reading_List.query.filter(Reading_List.comic_id == comic_id, Reading_List.user_id == user_id).first()

    db.session.delete(reading_list_comic)
    db.session.commit()

    return jsonify(message='deleted')



