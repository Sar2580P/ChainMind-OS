import json
import os
import logging
from concurrent.futures import ThreadPoolExecutor
from pydantic import BaseModel, Field
from ai_workflow.return_schema import CodePlanner_Level3
from pydantic_ai import RunContext, Agent
from typing import Dict, Set
from ai_workflow.utils import get_llm
from ai_workflow.return_schema import CodeBlock
from tqdm import tqdm
import asyncio

# Configure logger
logging.basicConfig(
    level=logging.DEBUG,  # You can change the level to INFO, WARNING, ERROR based on needs
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

class SM_CODER(BaseModel):
    save_dir: str
    retries: int = 2
    available_parallel_coders: Set[int] = Field(default=set(), description="Set of available parallel coders.")
    max_parallel_coders: int = Field(default=0, description="Maximum number of parallel coders.")
    llm_model_name: str = Field(..., description="Name of the LLM model to use.")

    def __init__(self, save_dir: str, max_parallel_coders: int, llm_model_name: str, retries: int = 1, **kwargs):
        # Pass the arguments to the BaseModel constructor properly
        super().__init__(save_dir=save_dir, max_parallel_coders=max_parallel_coders, 
                         llm_model_name=llm_model_name, retries=retries, **kwargs)
        
        self.save_dir = save_dir
        os.makedirs(self.save_dir, exist_ok=True)  
        self.retries = retries
        self.max_parallel_coders = max_parallel_coders
        self.available_parallel_coders = set(range(self.max_parallel_coders))  # Initialize the set of coders
        
        logger.info(f"SM_CODER initialized with max_parallel_coders={self.max_parallel_coders}, "
                    f"save_dir={self.save_dir}, llm_model_name={self.llm_model_name}")
        
    def get_available_coder(self):
        if len(self.available_parallel_coders) > 0:
            coder_idx = self.available_parallel_coders.pop()
            logger.debug(f"Coder {coder_idx} is now in use.")
            return get_llm(model_name=self.llm_model_name, idx= coder_idx), coder_idx
        else:
            raise Exception("No available coder found.")
        
    def get_coder_agent(self):
        llm, coder_idx = self.get_available_coder()
        agent = Agent(model=llm, retries=self.retries)
        return agent, coder_idx
        

    def generate_code_for_file(self, full_file_path: str, global_objective: str, 
                               expert_signature: str, code_instructions: str , agent_id:str):
        """
        Generate code for a given file based on the instructions.
        The generated code is saved as a JSON with 'full_file_path' and 'full_code' as keys.
        """
        logger.info(f"Generating code for file: {full_file_path}")
        print(f"coder_idx: {self.available_parallel_coders}")
        coder, coder_idx = self.get_coder_agent()
        
        # Ensure there is an event loop for the current thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        @coder.system_prompt
        def write_code(ctx: RunContext[Dict[str, str]]) -> str:
            return f'''
            ROLE: {ctx.deps['role']}
            
            GLOBAL OBJECTIVE: {ctx.deps['global_objective']}
            
            EXPERT SIGNATURE: {ctx.deps['expert_signature']}
            
            CODE INSTRUCTIONS: {ctx.deps['code_instructions']}
            
            You need to write the code for the file: {ctx.deps['full_file_path']}
            Code: ``` ....```
        '''
        
        # try:
        role = '''
        You are expert **Software Developer** specializing in **Smart Contracts** development.
        You need to implement the code for smart_contracts in solidity from the viewpoint of expert_signature.
        '''
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = coder.run_sync( user_prompt="Generate code...", 
                                deps={"role": role, "global_objective": global_objective, 
                                      "full_file_path": full_file_path,
                                        "expert_signature": expert_signature, 
                                        "code_instructions": code_instructions})

        # Prepare the data to be saved
        code_data = {
            "expert_signature" : expert_signature ,
            "full_file_path": full_file_path,
            "full_code": response.data, 
            "objective_served" : global_objective
        }
        updated_file_name = "_".join(full_file_path.split(":")).split('.')[0]+'.json'
        save_path = os.path.join(self.save_dir, agent_id, "generated_codes", updated_file_name)

        # Save the code data as a JSON file
        with open(save_path, 'w') as json_file:
            json.dump(code_data, json_file, indent=4)
        
        logger.info(f"Code for {full_file_path} saved to {save_path}.")
            
        # except Exception as e:
        #     logger.error(f"Error generating code for {full_file_path}: {e}")
        
        # Add the coder back to the available coders
        self.available_parallel_coders.add(coder_idx)



    def generate_code_parallel(self, code_design: CodePlanner_Level3 , agent_id:str):
        """
        Generate code for all files in parallel using threading.
        """
        logger.info("Starting parallel code generation.")
        
        # Create a thread pool with a maximum number of threads
        with ThreadPoolExecutor(max_workers=self.max_parallel_coders) as executor:
            # Prepare the list of tasks
            tasks = []
            total_files = len(code_design.files)  # Get the total number of files
            
            for file_path, instruction in zip(code_design.files, code_design.code_instructions):
                # Submit the task to the thread pool
                tasks.append(
                    executor.submit(self.generate_code_for_file, file_path, code_design.global_objective, 
                                    code_design.expert_signature, instruction , agent_id)
                )
            
            # Use tqdm to track the progress of the tasks
            for _ in tqdm(tasks, total=total_files, 
                          desc=f"Code generation for : {code_design.global_objective}", unit="file"):
                # try:
                # Wait for task to complete and log success
                task = tasks.pop(0)
                task.result()  # This will raise an exception if the task failed
                logger.info(f"Task for {task} completed successfully.")
                # except Exception as e:
                #     logger.error(f"Error in task: {e}")
        
        logger.info("Parallel code generation completed.")
