from flask import Blueprint, jsonify
from scripts.services.bug_service import list_bugs

bugs_api = Blueprint("bugs_api", __name__)


@bugs_api.route("/bugs")
def bugs():

    return jsonify(list_bugs())