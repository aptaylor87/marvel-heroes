from models import Character, Comic, Reading_List, db 
from app import app 
from marvel import *

db.drop_all()
db.create_all()

get_all_characters()