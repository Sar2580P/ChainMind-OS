import os
from groq import Groq
from dotenv import load_dotenv
import yaml

def read_yaml(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data

def get_api_key():
    load_dotenv()
    return os.getenv("GROQ_API_KEY")

# client = Groq(
#     api_key=os.getenv("GROQ_API_KEY"),
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