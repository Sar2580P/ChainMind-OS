import logging
import threading
from pydantic import BaseModel, Field
from typing import List, Dict, Generator
from ai_workflow.return_schema import (DenseFiller_Level2, FullyDefinedObjective_Level2, 
                                       ObjectiveExtraction_Level1, CodePlanner_Level3, decorate)
from ai_workflow.ai_agents.agentic_land.base_expert import BaseExpert
from queue import Queue
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

'''
Tasks of orchestrator : 
1. Subscribe to all the experts assigned by level-1 agent for each objective.
2. Execute all experts asynchronously, filling in the DenseFiller_Level2 dataModel
3. Send to user sequentially all the model objects of DenseFiller_Level2, one by one, letting user provide the missing information.
4. Again call the expert to return the FullyDefinedObjective_Level2 dataModel for corresponding DenseFiller_Level2 dataModel.

'''
class OrchestratorLevel2(BaseModel):
    """ Orchestrator that manages reasoners and processes objectives """
    registered_expert_agents: Dict[str, "BaseExpert"] = Field({}, description="Dictionary of registered expert agents.")
    partial_design_bubble_count: Dict[str, int] = Field(default={}, description="Count of partial design bubbles for each expert.")
    IS_PARTIAL_STAGE_COMPLETED: bool = Field(default=False, description="Flag to check if partial stage is completed.")
    initial_plan: ObjectiveExtraction_Level1 = Field(default=None, description="Initial plan from level-1 agent.")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.registered_expert_agents = {}
        self.partial_design_bubble_count = {}
        self.IS_PARTIAL_STAGE_COMPLETED = False

    def create_experts_pool(self, reasoners: Dict[str, "BaseExpert"]):
        """ Allows users to register custom reasoners dynamically """
        self.registered_expert_agents.update(reasoners)
        logging.info(f"Registered reasoners: {list(self.registered_expert_agents.keys())}")

    def subscribe_tasks(self, data_object: ObjectiveExtraction_Level1) -> Dict[str, List]:
        """ Assigns objectives to the relevant singleton reasoners """
        logging.info("Subscribing to all the experts assigned by level-1 agent for each objective...")
        task_subscription = {name: [] for name in self.registered_expert_agents.keys()}

        for obj, context, experts in zip(
            data_object.objectives,
            data_object.brief_context_on_each_objective,
            data_object.tech_experts_for_objectives
        ):
            for reasoner_name in experts:
                if reasoner_name in self.registered_expert_agents:
                    task_subscription[reasoner_name].append((obj, context))
                else:
                    logging.warning(f"Reasoner '{reasoner_name}' not found in registered reasoners")

        return task_subscription

    def partial_design_objective(self, task_subscriptions: Dict[str, List]) -> None:
        """ Runs reasoners sequentially and collects results """
        logging.info("Executing reasoners sequentially...")

        for reasoner_name, tasks in task_subscriptions.items():
            self.partial_design_bubble_count[reasoner_name] = len(tasks)
            reasoner = self.registered_expert_agents[reasoner_name]
            
            # Sequentially execute reasoners
            for obj, context in tasks:
                reasoner.create_partially_designed_objective(obj, context)  # Filling in the DenseFiller_Level2 dataModel

        logging.info("All reasoners have completed execution.")
        return

    def fill_missing_design_params(self) -> Generator[FullyDefinedObjective_Level2, None, None]:
        """Generator that yields FullyDefinedObjective_Level2 objects from expert agents' queues."""
        
        for expert_agent_name, expert_agent in self.registered_expert_agents.items():
            partial_bubbles: Dict = expert_agent.get_partially_designed_objective_queue()
            for key, content in partial_bubbles.items():
                yield decorate(content), expert_agent_name
        self.IS_PARTIAL_STAGE_COMPLETED = True
        logging.info("All missing design parameters have been filled.")
        return
    
    def fully_designed_objective(self, expert_agent_name ,partial_design, user_guidance) -> None: 
        expert_agent = self.registered_expert_agents[expert_agent_name]
        expert_agent.create_fully_designed_objective(partial_design, user_guidance)
        return 
    
    def planning_codebase_workflow(self, objective, assigned_expert_name) -> CodePlanner_Level3:
        # full_designed_objectives_list: Dict[str, Queue[FullyDefinedObjective_Level2]] = {}
        
        expert_agent = self.registered_expert_agents[assigned_expert_name]
        plan = expert_agent.planning_codebase_workflow(objective)
        
        # # Collect the fully defined objectives queue for each expert agent
        # full_designed_objectives_list[assigned_expert_name] = expert_agent.get_fully_defined_objectives_queue()
        
        logging.info("Planning codebase workflow completed.")
        
        return plan
