from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from pydantic_ai.models.groq import GroqModel
from typing import Dict

class BaseExpert(BaseModel, ABC):
    """Abstract base class for all agent models."""
    model_config = {
        "arbitrary_types_allowed": True
    }
    # Abstract class variables (queues) that must be defined in child classes
    partially_designed_objective: Dict[str, BaseModel] = Field(default={})
    fully_defined_objectives: Dict[str, BaseModel] = Field(default={})
    code_planner: Dict[str, BaseModel] = Field(default={})
    llm: GroqModel
    retries: int = 4


    @abstractmethod
    def create_partially_designed_objective(self, objective, context):
        pass
    
    @abstractmethod
    def create_fully_designed_objective(self, partial_design, user_guidance):
        """
        Abstract method to create a fully designed objective based on partial design and user guidance.
        
        :param partial_design: The partially designed object (could be any object or model), 
                                extracted for objective available from initial user input.
        :param user_guidance: Extra information provided by the user to help in designing the objective.
        """
        pass
    
    @abstractmethod
    def planning_codebase_workflow(self)->int:
        '''
        Returns: the len of remaining fully_defined_objectives_queue 
        '''
        pass

    def get_fully_defined_objectives_queue(self) -> Dict[str, BaseModel]:
        """Getter method for fully_defined_objectives."""
        return self.fully_defined_objectives
    
    def get_partially_designed_objective_queue(self) -> Dict[str, BaseModel]:
        """Getter method for partially_designed_objective."""
        return self.partially_designed_objective