import asyncio

import gradio as gr
from dotenv import load_dotenv
from manager import Manager


async def execute():
    # create instance of ResearchManager
    m = Manager()

    # run it
    print("running the agent")
    await m.run()


load_dotenv()
asyncio.run(execute())

# with gr.Blocks(theme=gr.themes.Default(primary_hue="sky")) as ui:
#    gr.Markdown("This is a test")
#    txtbx = gr.Textbox(label="type something")
#    btn = gr.Button("Clicker")
#    out = gr.Markdown(label="outputs")
#
#    btn.click(fn=execute, inputs=txtbx, outputs=out)
#
# ui.launch()
