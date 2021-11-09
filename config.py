#configuration file
import os
from flask import Flask

basedir = os.path.abspath(os.path.dirname(__file__))
WTF_CSRF_ENABLED = True
SECRET_KEY = 'g8y2g3fr6g8g84t3gyw8yg'