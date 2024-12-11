import os
from datetime import timedelta

class Config:
    SECRET_KEY = 'dev'  # Change this to a random string in production
    SQLALCHEMY_DATABASE_URI = 'sqlite:///devconnect.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
