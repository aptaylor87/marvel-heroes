from unittest import TestCase
from app import app,  CURR_USER_KEY
from models import db, Character, User, Comic, Reading_List
from marvel import *

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///marvel_app_test'
app.config['SQLAlCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class SearchViewsTestCase(TestCase):
    """Test Views for searches"""
    
    def setUp(self):

        Character.query.delete()

        character1 = Character(id=1009718, name="Wolverine")
        character2 = Character(id=1009417, name="Wolverine")

        db.session.add(character1)
        db.session.add(character2)

        db.session.commit()

    def tearDown(self):
        db.session.rollback()

    def test_search_form_view(self):
        with app.test_client() as client:
            resp = client.get("/")
            

            self.assertEqual(resp.status_code, 200)

    def test_search_form_results(self):
        with app.test_client() as client:
            resp = client.get("/search_results/1009718/1009417/20/2649")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Wolverine', html)

class Reading_ListViewTestCase(TestCase):
    """Test views for reading_lists"""
    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Comic.query.delete()

        self.client = app.test_client()

        self.testuser1 = User.register(username="testuser1",
                                    password="testuser1")
        
        self.comic = Comic(id=1, title='Comic Name', description="This is a hero.", marvel_url="test_url", image_url="test_image_url", image_type=".jpg")

        db.session.add(self.comic)
        db.session.commit()

        self.reading_list = Reading_List(user_id=1, comic_id=1, character_one_name="hero1", character_two_name="hero2")

        db.session.add(self.reading_list)
        db.session.commit()
    

    def tearDown(self):
        """Clean up and fouled transaction"""

        db.session.rollback()

    def test_view_reading_list(self):

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser1.id

            resp = c.get(f"reading_list")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Comic Name', html)
            