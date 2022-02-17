from functools import wraps
from flask import Flask, jsonify
from flask import Response
from datetime import datetime
import traceback

from utils.converters import ResponseFormatter

def returns_json(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        res = ResponseFormatter()
        try:
            retval = f(*args, **kwargs)
            return res.success_response(retval)
        except Exception as e:
            res.set_response_code(500)
            if (len(e.args) > 1):
                res.set_error_code(e.args[0])
                res.set_error_message(e.args[1])
                if (len(e.args) > 2):
                    res.set_response_code(e.args[2])
            elif (len(e.args) == 1):
                # res.set_error_message(e.message)
                res.set_error_message(e.args[0])
            else:
                print(traceback.format_exc())
            return res.error_response()
    return decorated_function
