from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel
from ai_workflow.utils import read_yaml, get_api_key
from ai_workflow.return_schema import ObjectiveExtraction_Level1
from pydantic_ai import Agent, RunContext, ModelRetry

config = read_yaml('ai_workflow/config.yaml')['layer_0_params']
llm = GroqModel(model_name=config['llm_model'], api_key=get_api_key())
agent = Agent(model=llm, retries = config['retries'], result_type=ObjectiveExtraction_Level1)


@agent.system_prompt
def available_list_of_domain_experts(ctx: RunContext[str]) -> str:  
    return f'''Here is a list of experts to help in helping with user-needs regarding integrating blockchain in their domain
        {', '.join(ctx.deps['domain_experts'])}'''

@agent.system_prompt
def instructions_regarding_planning(ctx: RunContext[str]) -> str:
    return f'''Here are the instructions to help you with the planning:
    1. Identify the set of objectives user expects to achieve.
    2. Think about the set of experts needed to satisfy the objectives (at max 2 experts per objective).
'''

@agent.system_prompt
def role_as_product_manager(ctx: RunContext[str]) -> str:
    return f'''As a product manager, you need to identify the set of objectives user expects to achieve. 
    You only have the listed experts in team, so you need to plan accordingly.'''
        
@agent.system_prompt
def add_the_users_name(ctx: RunContext[str]) -> str:
    return f"The user's name is {ctx.deps['name']}."

USER_PROMPT = '''I am an administrator of a school, and I want to integrate blockchain for transparency and automation. 
We have teachers, students, and staff as stakeholders, and we need solutions for fee payments, 
salary disbursement, attendance tracking, report card verification, and a voting system for administrative decisions.
I want a step-by-step plan on how blockchain can help us, along with the required technology stack and execution plan.
'''

result = agent.run_sync(user_prompt=USER_PROMPT, 
                        deps={"name": "Sarvagya", "domain_experts": ["DAO", "NFTs", "DID"]})
print(result.data)

