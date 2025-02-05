import json
import os
import time
from ai_workflow.return_schema import ObjectiveExtraction_Level1, CodePlanner_Level3
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
    if isinstance(data, BaseModel):
        data = json.loads(data.model_dump_json())
    curr_dir = os.getcwd()
    if not os.path.exists(os.path.join(curr_dir, "database" , agent_id)):
        os.makedirs(os.path.join(curr_dir, "database" , agent_id))
    full_path = os.path.join(curr_dir, "database" , agent_id, file_name)
    with open(full_path, 'w') as f:
        json.dump(data, f)
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
config = read_yaml('ai_workflow/config.yaml')

def layer_1_objective_identification(USER_PROMPT: str , agent_id: str ):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    user_objectives = Level1_Agent.run_sync(user_prompt=USER_PROMPT, deps={"name": "Sarvagya", 
                                                                        "domain_experts": config['available_experts'],
                                                                        "max_experts_per_objective": config['layer_0_params']['max_experts_per_objective']})
    print(f"Identified User Objectives...")
    print(user_objectives.data)
    print("_"*50)
    return save_file_as_json('layer_1_objective_identification.json', agent_id, user_objectives.data)

def layer_feedback_objective_design(user_objectives_dict , agent_id: str):
    user_objectives_json = json.dumps(user_objectives_dict)
    user_objectives = ObjectiveExtraction_Level1.model_validate_json(user_objectives_json)

    orchestrator.create_experts_pool({'DAO_expert': dao_expert, 'NFT_expert': nft_expert, 
                                    'DID_expert': did_expert, 'DeFi_expert': defi_expert})
    task_subscriptions = orchestrator.subscribe_tasks(user_objectives)
    orchestrator.partial_design_objective(task_subscriptions)

    print("Partial design stage completed.")
    print(dao_expert.get_partially_designed_objective_queue().get())
    print("_"*50)

    gen = orchestrator.fill_missing_design_params()

    while True:
        try:
            (markdown_info_request, simple_info_request), expert_agent_name = next(gen)
            save_file_as_json('layer_feedback_objective_design.txt', agent_id, markdown_info_request)
            print("_"*50)
            print("Waiting for user response..." )
            print(markdown_info_request)
            
            start_time = time.time()
            while read_file_as_str('user_response_layer_feedback_objective_design.txt', agent_id) == None and time.time() - start_time < 60:
                time.sleep(10)
                print("Waiting for user response..." , time.time() - start_time)
                continue
            
            user_response = read_file_as_str('user_response.txt', agent_id) if read_file_as_str('user_response.txt', agent_id) else "Use Default Values and Proceed"
            orchestrator.fully_designed_objective(partial_design=simple_info_request, user_guidance=user_response, expert_agent_name=expert_agent_name)
        except StopIteration:
            print("Fully design stage completed.")
            break
        
    print(dao_expert.get_fully_defined_objectives_queue().get())
    
    return "Fully design stage completed."

def layer_2_agent_work_planning(agent_id: str):
    orchestrator = OrchestratorLevel2()
    solution_code_design_list:Dict[str, Queue] = orchestrator.planning_codebase_workflow()
    solution_code_design_dict = {}
    for expert_agent_name, objectives_code_design_queue in solution_code_design_list.items():
        solution_code_design_dict[expert_agent_name] = []
        while not objectives_code_design_queue.empty():
            solution_code_design_dict[expert_agent_name].append(objectives_code_design_queue.get())
    print("Codebase planning stage completed.")
    print(dao_expert.code_planner_queue.get())
    save_file_as_json('layer_2_agent_work_planning.json', agent_id, solution_code_design_dict)
    return solution_code_design_dict

def leayer_3_generate_codebase(agent_id: str , solution_code_design_list:Dict[str, Queue]):
    coder_config = read_yaml('ai_workflow/config.yaml')['coder_params']
    coder = SM_CODER(save_dir= coder_config['save_dir'], max_parallel_coders=coder_config['max_parallel_coders'], 
                    llm_model_name=coder_config['llm_model'], retries=coder_config['retries'])


    for expert_agent_name, objectives_code_design_queue in solution_code_design_list.items():
        while not objectives_code_design_queue.empty():
            code_design = objectives_code_design_queue.get()
            coder.generate_code_parallel(code_design=code_design , agent_id = agent_id)
            print("$"*10)
        print("_"*50)
        print(f"Completed all design implementations by expert: {expert_agent_name}")
        
    return "Codebase generation stage completed."
