import os
from dotenv import load_dotenv
import yaml
from pydantic_ai.models.groq import GroqModel
from groq import Groq

def read_yaml(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data

def get_api_key(idx:int=0):
    load_dotenv()
    api = os.getenv(f"GROQ_API_KEY_{idx}")
    return api

def get_llm(model_name="llama-3.3-70b-versatile" , idx=0):
    llm = GroqModel(model_name=model_name, api_key=get_api_key(idx))
    return llm

