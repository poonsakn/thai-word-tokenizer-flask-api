activate_this = '/var/www/pywordwrap/pywordwrap/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/pywordwrap/')
#try:
#    from pip._internal.operations import freeze
#except ImportError:  # pip < 10.0
#    from pip.operations import freeze
#
#x = freeze.freeze()
#for p in x:
#    print(p)
from pywordwrap import app as application
application.secret_key = 'anything you guess'

