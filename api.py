import os
from main import create_app, init_api, flaskrun

application = create_app()
application = init_api(application)

if __name__ == "__main__":
  flaskrun(application, default_port=application.config["PORT"], default_host=application.config["HOST"])
