from ai_workflow.ai_agents.agentic_land.base_expert import BaseExpert
from ai_workflow.return_schema import FullyDefinedObjective_Level2, DenseFiller_Level2, CodePlanner_Level3
from pydantic_ai import RunContext, ModelRetry, Agent
from typing import Dict, ClassVar
import asyncio

class DeFiExpert(BaseExpert):
    role: ClassVar[str] = "You are a DeFi expert. Use your expertise to design the solution."
    design_needs: ClassVar[str] = '''
                - Token Standard (e.g., ERC-20, ERC-721, ERC-1155)
                - Liquidity Pool Design (e.g., constant product, hybrid pools, AMM models)
                - Staking Mechanism (e.g., proof-of-stake, yield farming, liquidity mining)
                - Governance Mechanism (e.g., DAO, token-based voting)
                - Smart Contract Features (e.g., mintable, burnable, pausable, upgradable)
                - User Interface Requirements (e.g., Dapp design for interaction, wallet integration)
                - Security Features (e.g., multi-signature, auditing, circuit breakers)
                - Auditing and Compliance Requirements (e.g., KYC/AML for users, tax reporting)
                - Tokenomics (e.g., total supply, inflation/deflation mechanisms)
                - Interaction with External DeFi Protocols (e.g., lending platforms, aggregators)
            '''

    default_design_needs: ClassVar[str] = '''
                - Token Standard: ERC-20
                - Liquidity Pool Design: Constant Product
                - Staking Mechanism: Yield Farming, Liquidity Mining
                - Governance Mechanism: DAO with token-based voting
                - Smart Contract Features: Mintable, Burnable, Upgradable
                - User Interface Requirements: Dapp designed for seamless interaction with staking pools and governance features, integrated with wallets like MetaMask
                - Security Features: Multi-signature, regular audits, circuit breakers for emergency pauses
                - Auditing and Compliance Requirements: KYC/AML for user onboarding, tax reporting
                - Tokenomics: Total supply capped at 1 million tokens, deflationary model
                - Interaction with External DeFi Protocols: Integrated with lending platforms and aggregators for enhanced yield generation
            '''


    def create_partially_designed_objective(self, objective, context):
        agent = Agent(model=self.llm, retries=self.retries, result_type=DenseFiller_Level2)
        
        @agent.system_prompt
        def extract_design_needs(ctx:RunContext[Dict[str, str]])->str:
            return f'''
            ROLE: {ctx.deps['role']}
            
            DESIGN NEEDS: {ctx.deps['design_needs']}
            
            DEFAULT DESIGN NEEDS: {ctx.deps['default_design_needs']}
            
            You need to extract the custom design needs from the below user-provided objective and context:
                - Objective: {ctx.deps['objective']}
                - Context: {ctx.deps['context']}
        '''
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        res = agent.run_sync(result_type=DenseFiller_Level2, user_prompt="",
                        deps={"role": self.role, "design_needs": self.design_needs, 
                              "default_design_needs": self.default_design_needs, 
                              "objective": objective, "context": context})
        
        self.partially_designed_objective_queue.put(res.data)
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
        res = agent.run_sync(result_type=FullyDefinedObjective_Level2,user_prompt="",
                        deps={"role": self.role, "partial_design": partial_design, 
                              "default_design_needs": self.default_design_needs, 
                              "user_guidance": user_guidance})
        self.fully_defined_objectives_queue.put(res.data)
        return
    
    def planning_codebase_workflow(self)->int:
        if self.fully_defined_objectives_queue.empty():
            return 0
        else:
            obj = self.fully_defined_objectives_queue.get()
            role = '''
            You are an expert **Software Architecture Planner** specializing in **DeFi (Decentralized Finance)** smart contracts. 
            Your task is to plan the entire codebase, ensuring modularity, clarity, and separation of concerns.
            ----------------
            INSTRUCTIONS:
            - The rule for creating a file is-> separate dir using colon(:) --> `directory:subdirectory:filename.extension`
            - Maintain a clean separation between **core contracts, governance mechanisms, utilities, and interfaces**.
            - Utilize **interfaces** to enforce standard contract interactions.
            - Include necessary **utility contracts** for security and operational enhancements.
            '''

            agent = Agent(model=self.llm, retries=self.retries, result_type=CodePlanner_Level3)
            
            @agent.system_prompt
            def plan_codebase(ctx:RunContext[Dict[str, str]])->str:
                return f'''
                ROLE: {ctx.deps['role']}
                
                GLOBAL OBJECTIVE: {ctx.deps['full_defined_obj'].objective}
                CONTEXT: {ctx.deps['full_defined_obj'].brief_context_on_objective}
                
                SOLUTION DESIGN CONFIG: {ctx.deps['full_defined_obj'].solution_design_config}
            '''
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            res = agent.run_sync(result_type=CodePlanner_Level3, user_prompt="",
                        deps={"role": role, "full_defined_obj": obj})
            self.code_planner_queue.put(res.data)
            self.fully_defined_objectives_queue.task_done()
            return self.fully_defined_objectives_queue.qsize()
