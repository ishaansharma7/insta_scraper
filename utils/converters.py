from flask import Flask, render_template, redirect, jsonify, current_app, request, session, g, abort, Blueprint
from flask_paginate import Pagination
import re
import json
from mongoengine.queryset.visitor import Q
from werkzeug.routing import BaseConverter, ValidationError
from itsdangerous import base64_encode, base64_decode
from bson.objectid import ObjectId
from bson.errors import InvalidId
from random import randint
import httplib2


class ObjectEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "to_json"):
            return self.default(obj.to_json())
        elif hasattr(obj, "__dict__"):
            d = dict(
                (key, value)
                for key, value in inspect.getmembers(obj)
                if not key.startswith("__")
                and not inspect.isabstract(value)
                and not inspect.isbuiltin(value)
                and not inspect.isfunction(value)
                and not inspect.isgenerator(value)
                and not inspect.isgeneratorfunction(value)
                and not inspect.ismethod(value)
                and not inspect.ismethoddescriptor(value)
                and not inspect.isroutine(value)
            )
            return self.default(d)
        return obj


class ResponseFormatter():
    def __init__(self):
        self.response_code = 200
        self.error_code = 101
        self.error_message = "Unhandled rejection. Please try after some time or contact admin"
        self.formatted_result = {
            "code": self.response_code,
            "status": "success",
            "error": False,
            "error_code": None,
            "reason": "",
            "data": None
        }

    def set_response_code(self, code):
        self.response_code = code

    def set_error_code(self, code):
        self.error_code = code

    def set_error_message(self, message):
        self.error_message = message

    def success_response(self, data=None):
        if data:
            self.formatted_result["data"] = dict()
            self.formatted_result["data"]["result"] = data

        return jsonify(self.formatted_result), self.response_code

    def error_response(self):
        self.formatted_result["code"] = self.response_code
        self.formatted_result["status"] = "failure"
        self.formatted_result["error"] = True
        self.formatted_result["error_code"] = self.error_code
        self.formatted_result["reason"] = self.error_message

        return jsonify(self.formatted_result), self.response_code
