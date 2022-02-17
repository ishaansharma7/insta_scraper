from flask import Flask, url_for, render_template, redirect, jsonify, current_app, session, g, abort, Blueprint
import os
import random
import datetime
import importlib
# import redis as sRedis
import optparse
from extensions import dbt


def create_app():
   application = Flask(__name__)
   application.config.from_pyfile(".env")
   for i in application.config:
      os.environ[i] = str(application.config[i])
   dbt.init_app(application)


   return application

def init_api(application):
   for i in application.config:
      os.environ[i] = str(application.config[i])

   import views
   for path, blueprint, url_prefix in views.blueprints:
      module = importlib.import_module(path)
      application.register_blueprint(getattr(module, blueprint), url_prefix=url_prefix)

   return application

def flaskrun(app, default_host="127.0.0.1",
                  default_port="5000"):
    """
    Takes a flask.Flask instance and runs it. Parses
    command-line flags to configure the app.
    """

    # Set up the command-line options
    parser = optparse.OptionParser()
    parser.add_option("-H", "--host",
                      help="Hostname of the Flask app " + \
                           "[default %s]" % default_host,
                      default=default_host)
    parser.add_option("-P", "--port",
                      help="Port for the Flask app " + \
                           "[default %s]" % default_port,
                      default=default_port)

    # Two options useful for debugging purposes, but
    # a bit dangerous so not exposed in the help message.
    parser.add_option("-d", "--debug",
                      action="store_true", dest="debug",
                      help=optparse.SUPPRESS_HELP)
    parser.add_option("-p", "--profile",
                      action="store_true", dest="profile",
                      help=optparse.SUPPRESS_HELP)

    options, _ = parser.parse_args()

    # If the user selects the profiling option, then we need
    # to do a little extra setup
    if options.profile:
        from werkzeug.contrib.profiler import ProfilerMiddleware

        app.config['PROFILE'] = True
        app.wsgi_app = ProfilerMiddleware(app.wsgi_app,
                       restrictions=[30])
        options.debug = True

    app.run(
        debug=options.debug,
        host=options.host,
        port=int(options.port)
    )
