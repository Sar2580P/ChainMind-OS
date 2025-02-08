import json
import os
import time
from ai_workflow.return_schema import ObjectiveExtraction_Level1, CodePlanner_Level3, decorate_objective
from ai_workflow.ai_agents.layer_2.orchestrator import OrchestratorLevel2
from ai_workflow.ai_agents.agentic_land.dao_expert import DAOExpert
from ai_workflow.ai_agents.agentic_land.base_expert import BaseExpert
from ai_workflow.ai_agents.agentic_land.did_expert import DIDExpert
from ai_workflow.ai_agents.agentic_land.nft_expert import NFTExpert
from ai_workflow.ai_agents.agentic_land.defi_expert import DeFiExpert

from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel
from ai_workflow.utils import read_yaml, get_api_key, get_llm
from ai_workflow.return_schema import ObjectiveExtraction_Level1
from pydantic_ai import Agent, RunContext, ModelRetry
import asyncio
from ai_workflow.ai_agents.layer_3.smart_contracts_coder_expert import SM_CODER
from typing import Dict
from queue import Queue
from ai_workflow.ai_agents.layer_1.agents import agent as Level1_Agent
from pydantic import BaseModel

def save_file_as_json(file_name,agent_id, data):
    if file_name.endswith('.txt'):
        curr_dir = os.getcwd()
        if not os.path.exists(os.path.join(curr_dir, "database" , agent_id)):
            os.makedirs(os.path.join(curr_dir, "database" , agent_id))
        full_path = os.path.join(curr_dir, "database" , agent_id, file_name)
        with open(full_path, 'w') as f:
            f.write(data) 
        return data
    if isinstance(data, BaseModel):
        data = data.model_dump()
        
    curr_dir = os.getcwd()
    if not os.path.exists(os.path.join(curr_dir, "database" , agent_id)):
        os.makedirs(os.path.join(curr_dir, "database" , agent_id))
    full_path = os.path.join(curr_dir, "database" , agent_id, file_name)
    with open(full_path, 'w') as f:
        f.write(json.dumps(data, indent=4)) 
    return data

def read_file_as_str(file_name, agent_id):
    curr_dir = os.getcwd()
    full_path = os.path.join(curr_dir, "database" , agent_id, file_name)
    
    if not os.path.exists(full_path):
        return None
    with open(full_path, 'r') as f:
        file_data = f.read()
        os.remove(full_path)
        return file_data
    return None

llm = get_llm()
orchestrator = OrchestratorLevel2()
dao_expert = DAOExpert(llm = llm)
nft_expert = NFTExpert(llm = llm)
did_expert = DIDExpert(llm = llm)
defi_expert = DeFiExpert(llm= llm)
orchestrator = OrchestratorLevel2()
config = read_yaml('ai_workflow/config.yaml')

def layer_1_objective_identification(USER_PROMPT: str , agent_id: str ):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    user_objectives = Level1_Agent.run_sync(user_prompt=USER_PROMPT, deps={"name": "Sarvagya", 
                                                                        "domain_experts": config['available_experts'],
                                                                        "max_experts_per_objective": config['layer_0_params']['max_experts_per_objective']})
    print(f"Identified User Objectives...")
    print("_"*50)
    orchestrator.initial_plan = user_objectives.data
    markdown_text = decorate_objective(user_objectives.data)
    return save_file_as_json('layer_1_objective_identification.json', agent_id, user_objectives.data), markdown_text

def layer_feedback_objective_design(user_objectives_dict , agent_id: str):
    print(user_objectives_dict)
    user_objectives = ObjectiveExtraction_Level1(**user_objectives_dict)
    orchestrator.create_experts_pool({'DAO_expert': dao_expert, 'NFT_expert': nft_expert, 
                                    'DID_expert': did_expert, 'DeFi_expert': defi_expert})
    task_subscriptions = orchestrator.subscribe_tasks(user_objectives)
    orchestrator.partial_design_objective(task_subscriptions)
    print("Partial design stage completed.")
    print("_"*50)

    gen = orchestrator.fill_missing_design_params()
    while True:
        try:
            (markdown_info_request, simple_info_request), expert_agent_name = next(gen)
            save_file_as_json('layer_feedback_objective_design.txt', agent_id, markdown_info_request)
            print("_"*50)
            print("Waiting for user response..." )            
            start_time = time.time()
            while read_file_as_str('user_response_layer_feedback_objective_design.txt', agent_id) == None and time.time() - start_time < 60:
                time.sleep(10)
                print("Waiting for user response..." , time.time() - start_time)
                continue
            
            user_response = read_file_as_str('user_response.txt', agent_id) if read_file_as_str('user_response.txt', agent_id) else "Use Default Values and Proceed"
            orchestrator.fully_designed_objective(partial_design=simple_info_request, 
                                                  user_guidance=user_response, 
                                                  expert_agent_name=expert_agent_name)
        except StopIteration:
            print("Fully design stage completed.")
            break
        
    return "Fully design stage completed."

def layer_2_agent_work_planning(agent_id: str, id: str):
    objective_idx, assigned_expert_idx = id.split("_")[-2], id.split("_")[-1]    # objective_idx, assigned_expert_idx are 1-indexed 
    objective = orchestrator.initial_plan.objectives[int(objective_idx)-1]
    assigned_expert_name = orchestrator.initial_plan.tech_experts_for_objectives[int(objective_idx)-1][int(assigned_expert_idx)-1]
    
    solution_code_design:CodePlanner_Level3 = orchestrator.planning_codebase_workflow(objective, assigned_expert_name)
    
    print("Codebase planning stage completed.")
    return save_file_as_json(f'layer_2_agent_work_planning_{id}.json', agent_id, solution_code_design)

def leayer_3_generate_codebase(agent_id: str , solution_code_design_dict:Dict):
    coder_config = read_yaml('ai_workflow/config.yaml')['coder_params']
    coder = SM_CODER(save_dir= coder_config['save_dir'], max_parallel_coders=coder_config['max_parallel_coders'], 
                    llm_model_name=coder_config['llm_model'], retries=coder_config['retries'])

    code_design = CodePlanner_Level3(**solution_code_design_dict)
    coder.generate_code_parallel(code_design=code_design , agent_id = agent_id)
        
    return "Codebase generation stage completed."
