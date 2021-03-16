activate_this = '/var/www/pywordwrap/pywordwrap/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/pywordwrap/')

from pywordwrap import app as application
application.secret_key = 'anything you guess'

