# define the models we are using in this project
from agents import AsyncOpenAI, OpenAIChatCompletionsModel

# OPENAI MODELS
GPT_4_1_MINI = "gpt-4.1-mini"

# OLLAMA MODELS
ollama_base_url = "http://localhost:11434/v1"
o_client = AsyncOpenAI(base_url=ollama_base_url, api_key="ollama")
LLAMA_3_2 = OpenAIChatCompletionsModel(model="llama3.2", openai_client=o_client)
