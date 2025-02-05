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


llm = get_llm()
config = read_yaml('ai_workflow/config.yaml')
USER_PROMPT = '''I am an administrator of a school, and I want to integrate blockchain for transparency and automation. 
We have teachers, students, and staff as stakeholders, and we need solutions for fee payments, 
salary disbursement and a voting system for administrative decisions.
I want a step-by-step plan on how blockchain can help us, along with the required technology stack and execution plan.
'''

user_objectives = Level1_Agent.run_sync(user_prompt=USER_PROMPT, deps={"name": "Sarvagya", 
                                                                       "domain_experts": config['available_experts'],
                                                                       "max_experts_per_objective": config['layer_0_params']['max_experts_per_objective']})
print(f"Identified User Objectives...")
print(user_objectives.data)
print("_"*50)

orchestrator = OrchestratorLevel2()
dao_expert = DAOExpert(llm = llm)
nft_expert = NFTExpert(llm = llm)
did_expert = DIDExpert(llm = llm)
defi_expert = DeFiExpert(llm= llm)

orchestrator.create_experts_pool({'DAO_expert': dao_expert, 'NFT_expert': nft_expert, 
                                  'DID_expert': did_expert, 'DeFi_expert': defi_expert})
task_subscriptions = orchestrator.subscribe_tasks(user_objectives.data)
orchestrator.partial_design_objective(task_subscriptions)

print("Partial design stage completed.")
print(dao_expert.get_partially_designed_objective_queue().get())
print("_"*50)

gen = orchestrator.fill_missing_design_params()

while True:
    try:
        (html_info_request, simple_info_request), expert_agent_name = next(gen)
        user_response = "Hare Krishna Hare Ram"
        orchestrator.fully_designed_objective(partial_design=simple_info_request, user_guidance=user_response, expert_agent_name=expert_agent_name)
    except StopIteration:
        print("Fully design stage completed.")
        break
    
print(dao_expert.get_fully_defined_objectives_queue().get())

# working towards the planning_codebase_workflow
solution_code_design_list:Dict[str, Queue] = orchestrator.planning_codebase_workflow()
print("Codebase planning stage completed.")
print(dao_expert.code_planner_queue.get())


coder_config = read_yaml('ai_workflow/config.yaml')['coder_params']
coder = SM_CODER(save_dir= coder_config['save_dir'], max_parallel_coders=coder_config['max_parallel_coders'], 
                 llm_model_name=coder_config['llm_model'], retries=coder_config['retries'])


for expert_agent_name, objectives_code_design_queue in solution_code_design_list.items():
    while not objectives_code_design_queue.empty():
        code_design = objectives_code_design_queue.get()
        coder.generate_code_parallel(code_design=code_design)
        print("$"*10)
    print("_"*50)
    print(f"Completed all design implementations by expert: {expert_agent_name}")

        
'''
Partial design stage completed.
objective='transparency and automation of fee payments' brief_context_on_objective='The user wants to create a transparent and automated system for fee payments using blockchain' what_is_provided=['objective', 'context'] 
what_is_missing=['custom voting type', 'custom quorum percentage', 'custom decision threshold', 'custom on-chain voting preference', 'custom voting duration'] 
default_filler={'voting_type': 'one-person-one-vote', 'quorum_percentage': '50%', 'decision_threshold': '50%', 'on_chain_voting': 'true', 'voting_duration': '7'} expert_signature='DAO Expert'
'''
'''
Fully design stage completed.
objective='transparent and automated salary disbursement' brief_context_on_objective='The user is looking to automate salary disbursement using blockchain-based smart contracts, aiming for transparency and timely payments.' 
solution_design_config={'voting_type': 'one-person-one-vote', 'quorum_percentage': '50%', 'decision_threshold': '50%', 'on_chain_voting': 'true', 'voting_duration': '7'} expert_signature='DAO Expert'
'''

'''
global_objective='Securely verify report cards using a DAO',
files=['contracts:dao:dao.sol', 'contracts:interfaces:idao.sol', 'contracts:reportcard:reportcardverifier.sol', 'contracts:utilities:erc721tokenuri.sol'], 
code_instructions=['Create a DAO contract in contracts:dao:dao.sol that implements the proposed voting mechanism, using the provided SOLUTION DESIGN CONFIG. This contract should inherit from the OpenZeppelin Governor contract and implement the Idao interface.', 'Implement the idao interface in contracts:interfaces:idao.sol. The idao interface should include functions for proposing, voting, and executing proposals.', 'Create a ReportCardVerifier contract in contracts:reportcard:reportcardverifier.sol that will handle report card verification. This contract should be owned by the DAO and only executable by the DAO.', 'Create a utility contract in contracts:utilities:erc721tokenuri.sol for generating token URIs for report cards.'],
expert_signature='Dr. SmartContract'
'''


coder_config = read_yaml('ai_workflow/config.yaml')['coder_params']

data_module = CodePlanner_Level3(global_objective='Securely verify report cards using a DAO',
files=['contracts:dao:dao.sol', 'contracts:interfaces:idao.sol', 'contracts:reportcard:reportcardverifier.sol', 'contracts:utilities:erc721tokenuri.sol'], 
code_instructions=['Create a DAO contract in contracts:dao:dao.sol that implements the proposed voting mechanism, using the provided SOLUTION DESIGN CONFIG. This contract should inherit from the OpenZeppelin Governor contract and implement the Idao interface.', 'Implement the idao interface in contracts:interfaces:idao.sol. The idao interface should include functions for proposing, voting, and executing proposals.', 'Create a ReportCardVerifier contract in contracts:reportcard:reportcardverifier.sol that will handle report card verification. This contract should be owned by the DAO and only executable by the DAO.', 'Create a utility contract in contracts:utilities:erc721tokenuri.sol for generating token URIs for report cards.'],
expert_signature='Dr. SmartContract')
coder = SM_CODER(save_dir= coder_config['save_dir'], max_parallel_coders=coder_config['max_parallel_coders'], 
                 llm_model_name=coder_config['llm_model'], retries=coder_config['retries'])

coder.generate_code_parallel(code_design=data_module)

