from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()


class Character(db.Model):
    """Character."""

    __tablename__ = 'characters'

    id = db.Column(db.Integer,
                   primary_key=True)
    
    name = db.Column(db.String,
                     nullable=False)
    
    description = db.Column(db.String)
    
    marvel_url = db.Column(db.String)
    
    image_url = db.Column(db.String)

    image_type = db.Column(db.String)
    


class Comic(db.Model):
    """Comic."""

    __tablename__ = 'comics'

    id = db.Column(db.Integer,
                   primary_key=True)
    
    title = db.Column(db.String)
    
    description = db.Column(db.String)
    
    image_url = db.Column(db.String)

    image_type = db.Column(db.String)

    marvel_url = db.Column(db.String)

    
    
    

    


class Reading_List(db.Model):
    """Reading List."""

    __tablename__ = 'reading_list'
    
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        primary_key=True)

    comic_id = db.Column(db.Integer,
                         db.ForeignKey('comics.id'),
                         primary_key=True)

    character_one_name = db.Column(db.String)

    character_two_name = db.Column(db.String)

    # date_read = db.Column(db.Date)

    comic = db.relationship('Comic')

    def serialize_reading_list(self):
        return {
            "user_id": self.user_id,
            "comic_id": self.comic_id,
            "character_one_name": self.character_one_name,
            "character_two_name": self.character_two_name
        }

    

class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
    )

    username = db.Column(db.Text,
                         nullable=False,
                         unique=True,
    )

    password = db.Column(db.Text,
                         nullable=False,
    )

    comics = db.relationship('Comic', secondary="reading_list", backref="users")

    def __repr__(self):
        return f"<User #{self.id}: {self.username}>"
    
    def get_list_of_added_comics(self):
        comics_list = []
        for comic in self.comics:
            comics_list.append(comic.id)
        return comics_list


    @classmethod
    def register(cls, username, password):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = cls(
            username=username,
            password=hashed_pwd,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If it can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False
        
        

def connect_db(app):
    """Connects this database to provided Flask app."""

    db.app = app
    db.init_app(app)