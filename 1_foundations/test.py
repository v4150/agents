from os import _exit, getenv

from dotenv import load_dotenv
from openai import OpenAI


def main():
    load_dotenv()
    val = getenv("OPENAI_API_KEY")
    if val:
        print("Cool")
    else:
        print("oh noooo")
        _exit(1)

    # create client
    openai = OpenAI()

    # try to send a request
    messages = [
        {
            "role": "system",
            "content": "you are a chatbot and continue a conversation",
        },
        {
            "role": "user",
            "content": "That sounds great! I really enjoy hiking myself. There's something special about exploring new trails and taking in the scenery. Do you have a favorite outdoor activity or a particular spot you love to visit?",
        },
    ]

    response = openai.chat.completions.create(model="gpt-4.1-nano", messages=messages)

    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
