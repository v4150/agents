import time
from typing import List

import gradio as gr

messages = []  # history
markdown_history = ""


class DummyResponse:
    role: str
    content: str

    def __init__(self, role, content):
        self.role = role
        self.content = content


def run_markdown_test(input: str):
    global markdown_history
    markdown_history += f"\n# Your Input: \n\n{input}\n# My Input: \n\n"

    for (
        char
    ) in "this is a test response for some dummy testing that actually has no real meaning in terms of what it's saying":
        markdown_history += char
        time.sleep(0.05)
        yield markdown_history


def run(input: str):
    messages.append(
        {"role": "user", "content": input},
    )

    # set the dummy data to be sent...
    dummy_responses = [
        DummyResponse(
            role="assistant",
            content=f"Your input was '{input}', I will send my response immediately after this message...",
        ),
        DummyResponse(role="assistant", content="Hello There my Friend"),
    ]

    # actually send the dummy data, mimic a "processing" response
    for response in dummy_responses:
        messages.append({"role": response.role, "content": ""})
        for char in response.content:
            messages[-1]["content"] += char
            yield messages
            time.sleep(0.05)


with gr.Blocks() as ui:
    gr.Markdown("TESTING")
    user_input = gr.Textbox(label="Insert Text")
    # outputs = gr.Chatbot(type="messages")
    outputs = gr.Markdown()
    submit = gr.Button("GOGOGO")
    # submit.click(fn=run, inputs=[user_input], outputs=[outputs])
    submit.click(fn=run_markdown_test, inputs=user_input, outputs=outputs)

ui.launch()
