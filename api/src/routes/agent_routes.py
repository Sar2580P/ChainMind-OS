from flask import Blueprint, request
from src.utils.global_response import success_response, internal_server_error_response
from ai_workflow.ai_agents.main import (layer_1_objective_identification, layer_feedback_objective_design, 
                                        layer_2_agent_work_planning, leayer_3_generate_codebase)
from src.utils.utils import save_file_as_json, read_file_as_str

bp = Blueprint("agents", __name__)

@bp.route("/", methods=["GET"])
def get_all_agents():
    try:
        return success_response({"agents" :[]}, "Successfully retrieved all agents")
    except Exception as e:
        return internal_server_error_response(str(e))

@bp.route("layer_1_objective_identification/", methods=["POST"])
def layer_1_objective_identification_route():
    try:
        USER_PROMPT = request.json.get("USER_PROMPT")
        agent_id = request.json.get("new_agent_id")
        print(USER_PROMPT + " " + agent_id)
        response = layer_1_objective_identification(USER_PROMPT, agent_id)
        return success_response(response, "Successfully identified objectives")
    except Exception as e:
        return internal_server_error_response(str(e))

@bp.route("layer_feedback_objective_design/", methods=["POST"])
def layer_feedback_objective_design_route():
    try:
        print("Calling by api layer_feedback_objective_design")
        user_objectives_json = str(request.json.get("user_objectives_json"))
        agent_id = request.json.get("agent_id")
        response = layer_feedback_objective_design(user_objectives_json, agent_id)
        return success_response(response, "Successfully designed objectives")
    except Exception as e:
        return internal_server_error_response(str(e))

@bp.route("check_layer_feedback_objective_design/", methods=["POST"])
def check_layer_feedback_objective_design_route():
    try:
        print("Calling by api check_layer_feedback_objective_design")
        agent_id = request.json.get("agent_id")
        response = read_file_as_str('layer_feedback_objective_design.txt', agent_id)
        return success_response(response, "Successfully checked layer feedback objective design")
    except Exception as e:
        return internal_server_error_response(str(e))


@bp.route("check_user_response_layer_feedback_objective_design/", methods=["POST"])
def check_user_response_layer_feedback_objective_design_route():
    try:
        print("Calling by api check_user_response_layer_feedback_objective_design")
        agent_id = request.json.get("agent_id")
        response = save_file_as_json('user_response_layer_feedback_objective_design.txt', agent_id, request.json.get("user_response"))
        return success_response(response, "Successfully checked user response layer feedback objective design")
    except Exception as e:
        return internal_server_error_response(str(e))

@bp.route("layer_2_agent_work_planning/", methods=["POST"])
def layer_2_agent_work_planning_route():
    try:
        print("Calling by api layer_2_agent_work_planning")
        agent_id = request.json.get("agent_id")
        id = request.json.get("id")
        response = layer_2_agent_work_planning(agent_id)
        return success_response(response, "Successfully planned codebase workflow")
    except Exception as e:
        return internal_server_error_response(str(e))
    
@bp.route("leayer_3_generate_codebase/", methods=["POST"])
def leayer_3_generate_codebase_route():
    try:
        print("Calling by api leayer_3_generate_codebase")
        agent_id = request.json.get("agent_id")
        solution_code_design_list = request.json.get("solution_code_design_list")
        response = leayer_3_generate_codebase(agent_id, solution_code_design_list)
        return success_response(response, "Successfully generated codebase")
    except Exception as e:
        return internal_server_error_response(str(e))

@bp.route("get_codebase_for_file/", methods=["POST"])
def get_codebase_for_file_route():
    try:
        agent_id = request.json.get("agent_id")
        file_name = "generated_codes/" + request.json.get("file_name")
        response = read_file_as_str(file_name, agent_id)
        return success_response(response, "Successfully retrieved codebase for file")
    except Exception as e:
        return internal_server_error_response(str(e))