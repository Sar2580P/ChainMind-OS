from pydantic import BaseModel, Field, model_validator
from typing import List, Set, Dict, Union
from pydantic import BaseModel
from typing import List, Dict

from pydantic import BaseModel
from typing import List, Dict

from pydantic import BaseModel
from typing import List, Dict

def decorate(obj: BaseModel):
    # Use the recommended model_fields attribute to get model's fields
    attributes = obj.model_fields  # This gives the field names as keys in Pydantic V2
    html_decorated_string = ""
    plain_decorated_string = ""

    for attribute in attributes:
        value = getattr(obj, attribute)
        
        # Create HTML formatted heading for the attribute
        html_decorated_string += f"<h2 style='font-size: 20px; font-weight: bold;'>{attribute}:</h2>"
        
        # Create plain text formatted heading for the attribute
        plain_decorated_string += f"{attribute}:\n"

        if isinstance(value, list):
            # Format list items as a bulleted list for both HTML and plain text
            value_html = "\n".join([f"• {item}" for item in value])
            value_plain = "\n".join([f"• {item}" for item in value])
        else:
            value_html = value
            value_plain = value

        # Append the value after the heading
        html_decorated_string += f"<p>{value_html}</p>\n"
        plain_decorated_string += f"{value_plain}\n\n"
    
    return html_decorated_string, plain_decorated_string




class ObjectiveExtraction_Level1(BaseModel):
    objectives: List[str] = Field(..., description="List of objectives to be achieved.")
    brief_context_on_each_objective: List[str] = Field(..., description="Brief context for each objective.")
    tech_experts_for_objectives: List[Set[str]] = Field(..., description="Experts relevant to each objective.")

    @model_validator(mode="after")
    def check_list_lengths(self):
        """Ensures all three lists have the same length."""
        num_objectives = len(self.objectives)
        num_contexts = len(self.brief_context_on_each_objective)
        num_experts = len(self.tech_experts_for_objectives)

        if not (num_objectives == num_contexts == num_experts):
            raise ValueError(
                f"Mismatch in list lengths: objectives({num_objectives}), "
                f"contexts({num_contexts}), experts({num_experts}). "
                "All three must have the same length."
            )
        return self


class DenseFiller_Level2(BaseModel):
    objective: str 
    brief_context_on_objective: str 
    what_is_provided: List[str] = Field(
        ..., description="List of necessary information provided for designing the solution."
    )
    what_is_missing: List[str] = Field(
        ..., description="List of necessary information missing for designing the solution."
    )
    default_filler: Dict[str, str] = Field(
        ..., description="Default fallback options if certain required information is missing."
    )
    expert_signature: str = Field(
        ..., description="The name of the expert used."
    )

    @model_validator(mode="after")
    def check_list_lengths(self):
        """Ensures that what_is_missing and default_filler have the same length."""
        if len(self.what_is_missing) != len(self.default_filler):
            raise ValueError(
                f"Length mismatch: what_is_missing({len(self.what_is_missing)}) "
                f"and default_filler({len(self.default_filler)}) must be the same."
            )
        return self 

class FullyDefinedObjective_Level2(BaseModel):
    objective:str
    brief_context_on_objective:str
    solution_design_config : Dict[str, Union[str, int, float]] = Field(..., description="Full design config for the solution.")
    expert_signature: str
    
class CodePlanner_Level3(BaseModel):
    global_objective: str = Field(
        ..., description="The global objective of the code."
    )
    files: List[str] = Field(
        ..., description="List of files to be created for achieving the global objective."
    )
    code_instructions: List[str] = Field(
        ..., description="Prompt instruction for each file, guiding what code to write."
    )
    
    expert_signature: str = Field(
        ..., description="The name of the expert used."
    )

    @model_validator(mode="after")
    def check_list_lengths(self):
        """Ensures that `files` and `code_instructions` have the same length."""
        if len(self.files) != len(self.code_instructions):
            raise ValueError(
                f"Length mismatch: files({len(self.files)}) and code_instructions({len(self.code_instructions)}) must be the same."
            )
        return self  
    