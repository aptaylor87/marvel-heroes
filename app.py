from flask import Flask
import hashlib  #this is needed for the hashing library
import time   #this is needed to produce a time stamp
import json   #Marvel provides its information in json format
import requests #This is used to request information from the API

app = Flask(__name__)