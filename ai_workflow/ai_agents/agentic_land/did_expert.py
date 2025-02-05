from ai_workflow.ai_agents.agentic_land.base_expert import BaseExpert
from ai_workflow.return_schema import FullyDefinedObjective_Level2, DenseFiller_Level2, CodePlanner_Level3
from pydantic_ai import RunContext, ModelRetry, Agent
from typing import Dict, ClassVar
import asyncio

class DIDExpert(BaseExpert):
    role :  ClassVar[str] = "You are a Decentralized Identity (DID) expert. Use your expertise to design the solution."
    design_needs: ClassVar[str] = '''
                - DID Method (e.g., did:ethr, did:web, did:key)
                - Authentication Mechanism (e.g., public-private key, biometric, multi-factor authentication)
                - Key Rotation Policy (e.g., periodic, event-driven, manual)
                - Storage Type (on-chain/off-chain/hybrid)
                - Revocation Mechanism (e.g., smart contract, time-based, manual revocation)
                - Document Verification (whether document hashes are stored and verifiable on-chain)
                - DID Metadata Storage (on-chain or off-chain storage of metadata linked to DIDs)
                - Document Upload Mechanism (e.g., IPFS, Arweave)
                - Access Control (whether access control features are implemented in the smart contracts)
            '''

    default_design_needs: ClassVar[str] = '''
                - DID Method: did:web
                - Authentication Mechanism: public-private key
                - Key Rotation Policy: periodic
                - Storage Type: hybrid
                - Revocation Mechanism: smart contract
                - Document Verification: Yes (supports on-chain document verification using smart contracts)
                - DID Metadata Storage: Off-chain (metadata stored in JSON files, such as `did_1_metadata.json`)
                - Document Upload Mechanism: IPFS (documents are uploaded and linked via IPFS hashes)
                - Access Control: Yes (contract includes access control mechanisms to secure DID-related operations)
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
                - Objective : {ctx.deps['objective']}
                - Context : {ctx.deps['context']}
        '''
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        res = agent.run_sync(result_type=DenseFiller_Level2, user_prompt="" ,
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
        res = agent.run_sync(result_type=FullyDefinedObjective_Level2, user_prompt="",
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
            You are an expert **Software Architecture Planner** specializing in **DID (Decentralized Identifier) smart contracts** and **document verification** systems.
            Your task is to plan the entire codebase, ensuring modularity, clarity, and separation of concerns.
            ----------------
            INSTRUCTIONS:
            - The rule for creating a file is-> separate dir using colon(:) --> `directory:subdirectory:filename.extension`
            - Maintain a clean separation between **core contracts, metadata management, scripts, and utilities**.
            - Utilize **interfaces** where necessary for enforcing standard interactions across contracts.
            - Ensure **modular** design for scalability and maintainability, especially for DID creation, document verification, and cryptographic operations.

            '''
            agent = Agent(model=self.llm, retries=self.retries, result_type=CodePlanner_Level3)
            
            @agent.system_prompt
            def plan_codebase(ctx:RunContext[Dict[str, str]])->str:
                return f'''
                ROLE: {ctx.deps['role']}
                
                GLOBAL OBJECTIVE: {ctx.deps['full_defined_obj'].objective}
                CONTEXT :{ctx.deps['full_defined_obj'].brief_context_on_objective}
                
                SOLUTION DESIGN CONFIG: {ctx.deps['full_defined_obj'].solution_design_config}
            '''
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            res = agent.run_sync(result_type=CodePlanner_Level3, user_prompt="",
                        deps={"role": role, "full_defined_obj": obj})
            self.code_planner_queue.put(res.data)
            self.fully_defined_objectives_queue.task_done()
            return self.fully_defined_objectives_queue.qsize()