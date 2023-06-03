import pandas as pd
import gradio as gr
from fastapi import FastAPI, Request
import uvicorn
from pathlib import Path
FLAG_DIR = Path("./flagged")

logger = gr.CSVLogger()
logger.setup([gr.Text(label="URL"), gr.Text(label="Host")], FLAG_DIR)

# dummy data
websites = ['ABC', 'XYZ']

img = "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png"
websites = [[f'<img src="{img}" alt="" width="48" height="48" /><tr>1 cái chữ gì đó</tr>'] for x in websites]

df = pd.DataFrame(websites, columns=['img_code'])
df_html = df.to_html(escape=False, render_links=False,
                     index=False, header=False)

# create a FastAPI app
app = FastAPI()

components = gr.Image()
# gradio app
with gr.Blocks() as demo:
    gr.HTML(df_html)
    with gr.Row():
        pass

# custom get request handler with params to flag clicks
@app.get("/track")
async def track(url: str, request: Request):
    # host disable for privacy reasons
    # host = request.headers.get("host")
    logger.flag([url, "ip"])
    return {"message": "ok"}

# mount Gradio app to FastAPI app
app = gr.mount_gradio_app(app, demo, path="/")

# serve the app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)