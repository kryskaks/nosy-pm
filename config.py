from datetime import timedelta
import os

DEBUG = True

THREADS_PER_PAGE = 8

CSRF_ENABLED = True

SECRET_KEY = 'SeCmt#dnK!'

PERMANENT_SESSION_LIFETIME = timedelta(minutes=20)

DATABASE_URL = 'postgres://postgres:test@localhost/nosypm'

LOG_TO = "/home/kryskaks/nosy-pm/logs"

TMP_DIR = "/home/kryskaks/nosy-pm/tmp"