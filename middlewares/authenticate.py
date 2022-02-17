from functools import wraps
from flask import Flask, jsonify, request, current_app
from flask import Response
from datetime import datetime
import json
import traceback
from utils.user import get_user_data

# from extensions import cache
from utils.converters import ResponseFormatter

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = request.headers.get('id')
        user_token = request.headers.get('mc4ktoken')
        if user_id and user_token:
            try:
                user = get_user_data(user_id, user_token)
                if not user:
                    res = ResponseFormatter()
                    res.set_response_code(401)
                    res.set_error_code("MA002")
                    res.set_error_message("Unauthorized, invalid contact details")
                    return res.error_response()
                else:
                    request.user = user
                    return f(*args, **kwargs)
            except Exception as e:
                print(traceback.format_exc())
                res = ResponseFormatter()
                res.set_response_code(500)
                if (len(e.args) > 1):
                    res.set_error_code(e.args[0])
                    res.set_error_message(e.args[1])
                elif (len(e.args) == 1):
                    res.set_error_code('MA001')
                    res.set_error_message(e.message)
                return res.error_response()
        else:
            res = ResponseFormatter()
            res.set_response_code(401)
            res.set_error_code("MA003")
            res.set_error_message("Unauthorized, missing headers")
            return res.error_response()
    return decorated_function
