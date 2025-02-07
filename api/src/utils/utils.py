import os
import json
import random
import datetime
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

def update_json_file(agent_id, new_data):
    curr_dir = os.getcwd()
    agent_dir = os.path.join(curr_dir, "database", agent_id)
    file_path = os.path.join(agent_dir, "chat_history.json")
    
    if not os.path.exists(agent_dir):
        os.makedirs(agent_dir)
    
    if not os.path.exists(file_path):
        print("file_path", file_path)
        with open(file_path, 'w') as file:
            print("------------------use cha-----------------------")
            print(new_data)
            json.dump([new_data], file)
        return True
    else:
        with open(file_path) as file:
            print("------------------use cha-----------------------")
            print(new_data)
            data = json.load(file)
            data.append(new_data)
        with open(file_path, 'w') as file:
            json.dump(data, file)
        return True

def read_json_file(agent_id):
    curr_dir = os.getcwd()
    file_path = os.path.join(curr_dir, "database" , agent_id, "chat_history.json")
    if not os.path.exists(file_path):
        return []
    with open(file_path) as file:
        data = json.load(file)
    return data

def get_all_agnets_id():
    curr_dir = os.getcwd()
    database_path = os.path.join(curr_dir, "database")
    agents = [agent for agent in os.listdir(database_path) if os.path.isdir(os.path.join(database_path, agent))]
    return agents

def generate_random_id_from_uuid():
    char_set = "abcde_fghijklm_nopqrstuvwxyzABC_DEFGHIJKLMNOPQR_STUVWXYZ0123456789_"
    return ''.join(random.choice(char_set) for i in range(20))

def get_current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def read_code_json_file(file_name , agent_id):
    curr_dir = os.getcwd()
    file_path = os.path.join(curr_dir, "database" , agent_id, "generated_codes", file_name)
    print("file_path_code", file_path)
    if not os.path.exists(file_path):
        return "File not found"
    with open(file_path) as file:
        data = json.load(file)
    return data["full_code"]
