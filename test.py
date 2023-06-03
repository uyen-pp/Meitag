import gradio as gr
from itertools import chain

data_features = ['Checked', 'Image', 'Caption', 'Tags']
max_num_samples = 100

def refresh_dataset_ui(*dataset_ui):
    dataset_ui = [gr.update(value=None, visible=False, show_label=False) for _ in dataset_ui]
    return dataset_ui

def create_dataset_ui():
    dataset_view = []
    for _ in range(max_num_samples):
        with gr.Row():
            checked = gr.Checkbox(False, visible=False, show_label=False, interactive=True)
            with gr.Column(scale=1, min_width=60):
                img = gr.Image(visible=False, elem_classes='dataview_image')
            with gr.Column(scale=9):
                with gr.Row():
                    dummy_text = 'arkdown("<h3>Run Auto-captioning</h3>'
                    # path = gr.Textbox(dummy_text, visible=False, show_label=False, elem_classes='dataview_text')
                    capt = gr.Textbox(dummy_text, visible=False, show_label=False, elem_classes='dataview_text')
                    tags = gr.Textbox(dummy_text, visible=False, show_label=False, elem_classes='dataview_text')

        dataset_view.extend([checked, img, capt, tags])
    return dataset_view

def update_dataset_ui(image_files, progress=gr.Progress()):
    progress(0, "Updating...")
    if len(image_files) > max_num_samples:
        image_files = image_files[0: max_num_samples]

    checked = [gr.update(visible=True) for _ in image_files]
    images_update = [gr.update(value=image, visible=True) for image in image_files]
    # names_update = [gr.update(value=image.name, visible=True) for image in image_files]
    captions_update = [gr.update(value='', visible=True) for _ in image_files]
    tags_update = [gr.update(value='', visible=True) for _ in image_files]

    ret = list(chain(*zip(checked, images_update, captions_update, tags_update)))

    if len(image_files) < max_num_samples:
        ret.extend([
            gr.update
        ] * len(data_features) * (max_num_samples-len(image_files)))
    return ret

def add_samples(images):
    pass

with gr.Blocks(css='./style.css') as demo:
    current_dataset = gr.State([])
    with gr.Row():
        left, right = gr.Column(scale=2), gr.Column(scale=1)

        with left:
            # Dataview
            with gr.Row(elem_id='fixed_height'):
                table_ui = create_dataset_ui()

            # Actions
            with gr.Row():
                uploaded = gr.UploadButton(
                            label="Open Directory", 
                            file_types=['image'],
                            file_count='directory',
                            )
                
                added = gr.UploadButton(
                            label="Add Samples", 
                            file_types=['image'],
                            file_count='multiple',
                        )
                reset = gr.Button(
                            value="Select All", 
                        )
                reset = gr.Button(
                            value="Reset", 
                        )
                download = gr.Button(
                            value="Download Dataset", 
                        )

            uploaded.upload(refresh_dataset_ui, inputs=table_ui, outputs=table_ui
                            ).then(update_dataset_ui, inputs=uploaded, outputs=table_ui)

        with right:
            with gr.Row():
                editings = gr.Gallery()
            with gr.Row():
                save_editing = gr.Button(value="Save", variant='primary')
                cancel_editing = gr.Button(value="Cancel")

    with gr.Row():
        gr.Text("End of page")

demo.queue().launch()
