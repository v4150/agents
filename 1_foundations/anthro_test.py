from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic()

message = client.messages.create(
    model="claude-3-5-haiku-latest",
    max_tokens=500,
    messages=[
        {
            "role": "user",
            "content": "Name a sport that has been on the rise in the last three years",
        }
    ],
)

print(message.content)
