from flask import Blueprint, jsonify
import psutil
import os

system_api = Blueprint("system_api", __name__)


@system_api.route("/system")
def system_status():

    return jsonify({
        "cpu": psutil.cpu_percent(),
        "memory": psutil.virtual_memory().percent,
        "pid": os.getpid()
    })