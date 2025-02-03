from flask import Blueprint
from src.utils.global_response import success_response, internal_server_error_response

bp = Blueprint("agents", __name__)

@bp.route("/", methods=["GET"])
def get_all_agents():
    try:
        return success_response({"agents" :[]}, "Successfully retrieved all agents")
    except Exception as e:
        return internal_server_error_response(str(e))