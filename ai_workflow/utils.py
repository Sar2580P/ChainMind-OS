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
    print(model_name, get_api_key(idx), "***************************")
    llm = GroqModel(model_name=model_name, api_key=get_api_key(idx))
    return llm
# load_dotenv()
# client = Groq(
#     api_key=os.getenv("GROQ_API_KEY_0"),
# )

# chat_completion = client.chat.completions.create(
#     messages=[
#         {
#             "role": "user",
#             "content": "Write a stuti in hindi in lotusfeet of Sri Radha and Krishna",
#         }
#     ],
#     model="llama-3.3-70b-versatile",
# )

# print(chat_completion.choices[0].message.content)

