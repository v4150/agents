import gradio as gr
import time

def run(_str: str):
    output_list = [
            "Here's the first thing",
            "Here's the second thing",
            "Here's the third thing",
            "Here's the fourth thing",
            "Here's the fifth thing",
            "Here's the sixth thing",
            ]

    for output in output_list:
        time.sleep(5)
        print(output)
        yield output


with gr.Blocks(theme=gr.themes.Default(primary_hue="sky")) as ui:
    gr.Markdown("This is a test")
    input_text = gr.Textbox(label="Type something to test with")
    run_btn = gr.Button("Run it", variant="primary")
    _output = gr.Markdown(label="Test Output")

    run_btn.click(fn=run, inputs=input_text, outputs=_output)
    input_text.submit(fn=run, inputs=input_text, outputs=_output)

ui.launch(inbrowser=True)

