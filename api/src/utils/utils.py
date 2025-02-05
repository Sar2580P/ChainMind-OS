import os
import json
from pydantic import BaseModel


def save_file_as_json(file_name,agent_id, data):
    if isinstance(data, BaseModel):
        data = json.loads(data.model_dump_json())
    curr_dir = os.getcwd()
    if not os.path.exists(os.path.join(curr_dir, "database" , agent_id)):
        os.makedirs(os.path.join(curr_dir, "database" , agent_id))
    full_path = os.path.join(curr_dir, "database" , agent_id, file_name)
    with open(full_path, 'w') as f:
        json.dump(data, f)
    return data

def read_file_as_str(file_name, agent_id):
    curr_dir = os.getcwd()
    full_path = os.path.join(curr_dir, "database" , agent_id, file_name)
    print("full_path_api", full_path)
    
    if not os.path.exists(full_path):
        return None
    with open(full_path, 'r') as f:
        file_data = f.read()
        os.remove(full_path)
        return file_data
    return None