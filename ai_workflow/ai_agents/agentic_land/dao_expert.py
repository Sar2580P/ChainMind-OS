from ai_workflow.ai_agents.agentic_land.base_expert import BaseExpert
from ai_workflow.return_schema import FullyDefinedObjective_Level2, DenseFiller_Level2, CodePlanner_Level3
from pydantic_ai import RunContext, ModelRetry, Agent
from typing import Dict, ClassVar
import asyncio

class DAOExpert(BaseExpert):
    role: ClassVar[str]  = "You are a Decentralized Autonomous Organization (DAO) expert. Use your expertise to design the solution."
    design_needs: ClassVar[str] = '''
                - Voting Type (e.g., quadratic, token-weighted, one-person-one-vote)
                - Quorum Percentage (minimum percentage of votes required for a decision to be valid)
                - Decision Threshold (minimum percentage of votes needed for approval)
                - On-Chain Voting (true/false)
                - Voting Duration (in days)
                - Proposal Types (e.g., governance, funding, contract upgrades)
                - Proposal Execution (automatic/manual)
                - Voting Power Rules (e.g., token holdings, staked tokens)
                - Emergency Voting (true/false)
                - Delegated Voting (true/false)
            '''

    default_design_needs: ClassVar[str] = '''
                - Voting Type: one-person-one-vote
                - Quorum Percentage: 50%
                - Decision Threshold: 50%
                - On-Chain Voting: true
                - Voting Duration: 7 days
                - Proposal Types: governance, funding, contract upgrades
                - Proposal Execution: manual
                - Voting Power Rules: token holdings
                - Emergency Voting: false
                - Delegated Voting: false
            '''

    def create_partially_designed_objective(self, objective, context):
        agent = Agent(model=self.llm, retries=self.retries, result_type=DenseFiller_Level2)
        
        @agent.system_prompt
        def extract_design_needs(ctx:RunContext[Dict[str, str]])->str:
            return f'''
            ROLE: {ctx.deps['role']}
            
            DESIGN NEEDS: {ctx.deps['design_needs']}
            
            DEFAULT DESIGN NEEDS: {ctx.deps['default_design_needs']}
            
            You need to extract the custom_design needs from the below user provided objective and context:
                - Objective : {ctx.deps['objective']}
                - Context : {ctx.deps['context']}
        '''
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        res = agent.run_sync(result_type=DenseFiller_Level2, user_prompt="",
                        deps={"role": self.role, "design_needs": self.design_needs, 
                              "default_design_needs": self.default_design_needs, 
                              "objective": objective, "context": context})
        
        self.partially_designed_objective[objective] = res.data
        return
    

    def create_fully_designed_objective(self, partial_design, user_guidance):
        agent = Agent(model=self.llm, retries=self.retries, result_type=FullyDefinedObjective_Level2)
        
        @agent.system_prompt
        def extract_solution_settings(ctx:RunContext[Dict[str, str]])->str:
            return f'''
            ROLE: {ctx.deps['role']}
            
            PARTIAL DESIGN CONFIG: {ctx.deps['partial_design']}
            
            DEFAULT FULL DESIGN CONFIG: {ctx.deps['default_design_needs']}
            
            The user has provided the following guidance for designing the solution:
                - {ctx.deps['user_guidance']}
            
            You need to create a full design config from the partial design config, using user guidance (default fallback options can be used if necessary).
        '''
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        res = agent.run_sync(result_type=FullyDefinedObjective_Level2,user_prompt= "",
                        deps={"role": self.role, "partial_design": partial_design, 
                              "default_design_needs": self.default_design_needs, 
                              "user_guidance": user_guidance})
        self.fully_defined_objectives[res.data.objective] = res.data
        return
    

    def planning_codebase_workflow(self, objective:str)->CodePlanner_Level3:
        obj = self.fully_defined_objectives[objective]
        role = '''
        You are an expert **Software Architecture Planner** specializing in **DAO (Decentralized Autonomous Organization) smart contracts**. 
        Your task is to plan the entire codebase, ensuring modularity, clarity, and separation of concerns.
        ----------------
        INSTRUCTIONS:
        - The rule for creating a file is-> seperate dir using colon(:) --> `directory:subdirectory:filename.extension`
        - Maintain a clean separation between **core contracts, governance mechanisms, utilities, and interfaces**.
        - Utilize **interfaces** to enforce standard contract interactions.
        - Include necessary **utility contracts** for security and operational enhancements.
                    
        '''
        agent = Agent(model=self.llm, retries=self.retries, result_type=CodePlanner_Level3)
        @agent.system_prompt
        def plan_codebase(ctx:RunContext[Dict[str, str]])->str:
            return f'''
            ROLE: {ctx.deps['role']}
            ----------------
            GLOBAL OBJECTIVE: {ctx.deps['full_defined_obj'].objective}
            CONTEXT: {ctx.deps['full_defined_obj'].brief_context_on_objective}
            ----------------
            SOLUTION DESIGN CONFIG: {ctx.deps['full_defined_obj'].solution_design_config}
        
        '''
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        res = agent.run_sync(result_type=CodePlanner_Level3, user_prompt="",
                    deps={"role": role, "full_defined_obj": obj})
        self.code_planner[objective] = res.data
        return res.data
        