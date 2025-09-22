from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

class Evalulate(BaseModel):
    is_correct: bool
    feedback: str
    
load_dotenv()
openai = OpenAI()
messages = [{"role":"system", "content":"you are a math teacher, determine if the answers are correct and provide feedback, please."}, {"role":"user", "content": "6*3 is 4"}]

response = openai.beta.chat.completions.parse(
    model="gpt-4.1-nano",
    messages=messages,
    response_format=Evalulate
)

results =response.choices[0].message.parsed 
print(results)