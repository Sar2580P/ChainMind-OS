from ai_workflow.ai_agents.agentic_land.base_expert import BaseExpert
from ai_workflow.return_schema import FullyDefinedObjective_Level2, DenseFiller_Level2, CodePlanner_Level3
from pydantic_ai import RunContext, Agent
from typing import Dict, ClassVar

class NFTExpert(BaseExpert):
    role: ClassVar[str] = "You are an NFT expert. Use your expertise to design the solution."
    design_needs: ClassVar[str] = '''
                - Token Standard (e.g., ERC-721, ERC-1155, custom standard)
                - Minting Type (e.g., fixed supply, dynamic supply, on-demand minting)
                - Royalty Percentage (creator's earnings on secondary sales)
                - Storage Method (e.g., on-chain metadata, IPFS, centralized storage)
                - Smart Contract Features (e.g., burnable, transferable, time-locked)
                - Marketplace Integration (whether the token can be listed and traded on a marketplace)
                - License Agreement Support (whether the NFT includes a licensing agreement smart contract)
                - Patent Metadata (structure and storage of metadata, such as IPFS links to patent data)
            '''

    default_design_needs: ClassVar[str] = '''
                - Token Standard: ERC-721
                - Minting Type: Fixed Supply
                - Royalty Percentage: 5%
                - Storage Method: IPFS
                - Smart Contract Features: Transferable, Burnable
                - Marketplace Integration: Yes (supports listing and trading patents)
                - License Agreement Support: Yes (includes LicenseAgreement.sol)
                - Patent Metadata: Stored in IPFS with links to patent data
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
            You are an expert **Software Architecture Planner** specializing in **NFT (Non-Fungible Token) smart contracts** and **patent management** systems.
            Your task is to plan the entire codebase, ensuring modularity, clarity, and separation of concerns.
            ----------------
            INSTRUCTIONS:
            - The rule for creating a file is-> separate dir using colon(:) --> `directory:subdirectory:filename.extension`
            - Maintain a clean separation between **core contracts, marketplace mechanisms, royalty management, licensing agreements, and utilities**.
            - Utilize **interfaces** where necessary to enforce standard interactions across contracts.
            - Ensure **modular** design for scalability and maintainability, especially for minting patents, handling royalties, and managing licensing.
            - Include **deployment scripts** to facilitate easy deployment of contracts and interactions with them.
            - Organize **metadata** storage with standards (e.g., IPFS) for patent data and examples.
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
            
            res = agent.run_sync(result_type=CodePlanner_Level3, user_prompt="",
                        deps={"role": role, "full_defined_obj": obj})
            self.code_planner_queue.put(res.data)
            self.fully_defined_objectives_queue.task_done()
            return self.fully_defined_objectives_queue.qsize()