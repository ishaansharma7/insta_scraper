from flask import Flask, current_app, Blueprint
import traceback
from middlewares.return_json import returns_json
from urllib import parse
from middlewares.authenticate import token_required
boiler_plate_blueprint = Blueprint("boiler_plate_blueprint", __name__)



@boiler_plate_blueprint.route("/hello-world/", methods = ["GET"])
@returns_json
#@token_required
def hello_world():
    try:
        print("get Call >>>>>>")
        data = {"msg": "hello-world"}
    except Exception as e:
        data = {"msg": "Something went wrong"}
        traceback.print_exc()
    return data
