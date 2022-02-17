from datetime import datetime, timedelta
from flask import current_app
from main import create_app
import os
application = create_app()
import time
from scripts.test_script import hello_world


@application.cli.command('test_cmd')
def func_test_cmd():
   hello_world()