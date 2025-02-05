from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from queue import Queue
from pydantic_ai.models.groq import GroqModel

class BaseExpert(BaseModel, ABC):
    """Abstract base class for all agent models."""
    model_config = {
        "arbitrary_types_allowed": True
    }
    # Abstract class variables (queues) that must be defined in child classes
    partially_designed_objective_queue: Queue[BaseModel] = Field(default=Queue())
    fully_defined_objectives_queue: Queue[BaseModel] = Field(default=Queue())
    code_planner_queue: Queue[BaseModel] = Field(default=Queue())
    llm: GroqModel
    retries: int = 2


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

    def get_fully_defined_objectives_queue(self) -> Queue[BaseModel]:
        """Getter method for fully_defined_objectives_queue."""
        return self.fully_defined_objectives_queue
    
    def get_partially_designed_objective_queue(self) -> Queue[BaseModel]:
        """Getter method for partially_designed_objective_queue."""
        return self.partially_designed_objective_queue