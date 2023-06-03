import pandas as pd
import gradio as gr
from fastapi import FastAPI, Request
import uvicorn
from pathlib import Path
import os

# HF_TOKEN = os.environ.get("HF_TOKEN")
HF_TOKEN = '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'
FLAG_DIR = Path("./flagged")
DATASET_NAME = ""
# https://huggingface.co/datasets/radames/gradio_clicks_dataset

# setup logger
# remote logging to HuggingFace
remote = True
logger = gr.CSVLogger()
if remote:
    logger = gr.HuggingFaceDatasetSaver(
        HF_TOKEN, dataset_name=DATASET_NAME, organization=None, private=False)
logger.setup([gr.Text(label="URL"), gr.Text(label="Host")], FLAG_DIR)

# dummy data
websites = [
    ["https://www.google.com/"],
    ["https://www.youtube.com/"],
    ["https://www.facebook.com/"],
    ["https://www.wikipedia.org/"],
    ["https://www.amazon.com/"],
    ["https://www.yahoo.com/"],
    ["https://www.twitter.com/"],
    ["https://www.instagram.com/"],
    ["https://www.reddit.com/"],
    ["https://www.linkedin.com/"],
    ["https://www.netflix.com/"],
    ["https://www.microsoft.com/"],
    ["https://www.apple.com/"],
    ["https://www.zoom.us/"],
    ["https://www.gmail.com/"],
    ["https://www.dropbox.com/"],
    ["https://www.github.com/"],
    ["https://www.stackoverflow.com/"],
    ["https://www.medium.com/"],
    ["https://www.quora.com/"],
]

# add simple get request for tracking
websites = [
    [f"<a href={x[0]} target='_blank' onclick='fetch(\"/track?url={x[0]}\")'>{x[0]}</a>"] for x in websites]

df = pd.DataFrame(websites, columns=['img_code'])

df_html = df.to_html(escape=False, render_links=False,
                     index=False, header=False)

# create a FastAPI app
app = FastAPI()

# gradio app


def refresh():
    df = pd.read_csv(f"{FLAG_DIR}/{DATASET_NAME}/data.csv")
    url_counts = df.groupby('URL').count()['Host']
    normalized_counts = url_counts / url_counts.sum()
    return normalized_counts.to_dict()


with gr.Blocks() as block:
    gr.Markdown("""
    ## Gradio Tracking Clicks + FastAPI + HuggingFace Datasets
    This is a demo of how to track clicks on a Gradio app using FastAPI and HuggingFace Datasets.
    Each click sends a request to the FastAPI server, which logs the click to a HuggingFace dataset.
    """)
    with gr.Row():
        with gr.Column():
            refresh_bt = gr.Button("Refresh")
            gr.HTML(df_html)
        with gr.Column():
            labels = gr.Label()
    refresh_bt.click(fn=refresh, inputs=[], outputs=[labels])
    block.load(fn=refresh, inputs=[], outputs=[labels])
# custom get request handler to flag clicks


@ app.get("/track")
async def track(url: str, request: Request):
    # host disable for privacy reasons
    # host = request.headers.get("host")
    logger.flag([url, "ip"])
    return {"message": "ok"}

# mount Gradio app to FastAPI app
app = gr.mount_gradio_app(app, block, path="/")

# serve the app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
