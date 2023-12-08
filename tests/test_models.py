from unittest import TestCase
from app import app 
from models import db, connect_db, Character, User, Comic, Reading_List

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///marvel_app_test'
app.config['SQLAlCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class CharacterModelTestCase(TestCase):
    """Tests for model for Charcters"""

    def setUp(self):
        """Clear out and existing characters"""
        Character.query.delete()

    def tearDown(self):
        """Clean up any stuck transactions"""

        db.session.rollback()

    def test_character_model(self):
        """Does the basic model work?"""

        character = Character(id=1, name="Hero", description="This is a hero.", marvel_url="test_url", image_url="test_image_url", image_type=".jpg")

        db.session.add(character)
        db.session.commit()

        characters = Character.query.all()

        self.assertEqual(len(characters),1)

    def test_repr(self):
        """does __repr__ work"""

        character = Character(id=1, name="Hero", description="This is a hero.", marvel_url="test_url", image_url="test_image_url", image_type=".jpg")

        representation = character.__repr__()

        self.assertIn('Hero', representation)


class ComicModelTestCase(TestCase):
    """Tests for model for Charcters"""

    def setUp(self):
        """Clear out and existing characters"""
        Comic.query.delete()

    def tearDown(self):
        """Clean up any stuck transactions"""

        db.session.rollback()

    def test_comic_model(self):
        """Does the basic model work?"""

        comic = Comic(id=1, title='Comic Name', description="This is a hero.", marvel_url="test_url", image_url="test_image_url", image_type=".jpg")

        db.session.add(comic)
        db.session.commit()

        comics = Comic.query.all()

        self.assertEqual(len(comics),1)

    def test_repr(self):
        """does __repr__ work"""

        comic = Comic(id=1, title='Comic Name', description="This is a hero.", marvel_url="test_url", image_url="test_image_url", image_type=".jpg")

        representation = comic.__repr__()

        self.assertIn('Comic Name', representation)

class UserModelTestCase(TestCase):
    """Tests for model for users"""

    def setUp(self):
        """Clear out and existing users"""

        
        User.query.delete()
        Comic.query.delete()
        Reading_List.query.delete()

    def tearDown(self):
        """Clean up any stuck transactions"""

        db.session.rollback()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        users = User.query.all()

        self.assertEqual(len(users),1)

    def test_repr(self):
        """does __repr__ work"""

        u = User(
            username="testuser",
            password="HASHED_PASSWORD"
        )

        represenation = u.__repr__()

        self.assertIn('testuser',represenation)

    def test_register(self):
        u1 = User.register(username="testuser1", password="HASHED_PASSWORD")

        self.assertNotIn("HASHED_PASSWORD", u1.password)
        self.assertIn("testuser1", u1.username)

    def test_authenticate(self):

        u1 = User.register(
            username="testuser1",
            password="HASHED_PASSWORD",
        )

        db.session.commit()

        auth_user = User.authenticate("testuser1", "HASHED_PASSWORD")

        self.assertEqual(auth_user.username, "testuser1")
        self.assertNotEqual(auth_user.password, "HASHED_PASSWORD")

    


class Reading_ListrModelTestCase(TestCase):
    """Tests for model for reading_lists"""

    def setUp(self):
        """Clear out and existing reading lists"""
        Reading_List.query.delete()
        User.query.delete()
        Comic.query.delete()

    def tearDown(self):
        """Clean up any stuck transactions"""

        db.session.rollback()

    def test_reading_list_model(self):
        """does the basic movdel work"""

        user = User.register(
            username="testuser1",
            password="HASHED_PASSWORD",
        )

        comic = Comic(id=1, title='Comic Name', description="This is a hero.", marvel_url="test_url", image_url="test_image_url", image_type=".jpg")

        db.session.add(comic)
        db.session.commit()

        u1 = User.query.get(1)
        comic = Comic.query.get(1)

        reading_list = Reading_List(user_id=u1.id, comic_id=comic.id, character_one_name="hero1", character_two_name="hero2")
        db.session.add(reading_list)
        db.session.commit()

        reading_lists = Reading_List.query.all()
        self.assertEqual(len(reading_lists),1)
