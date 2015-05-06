from flask import Flask, session
from datetime import timedelta, date
import logging
import os
import config

app = Flask(__name__)

app.config.from_object('config')

logger = logging.getLogger("Nosy-PM")

if not os.path.exists(config.LOG_TO):
	os.makedirs(config.LOG_TO)

if not os.path.exists(config.TMP_DIR):
	os.makedirs(config.TMP_DIR)

# TODO from config
logger.setLevel(logging.DEBUG) 
filename = config.LOG_TO + "/log_{date:%Y-%m-%d}.log".format(date = date.today())		
fh = logging.FileHandler(filename)
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s[%(levelname)s] - %(name)s:%(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)
app.logger.addHandler(fh)

print "logger created"

import views