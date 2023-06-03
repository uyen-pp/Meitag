import gradio as gr
from typing import List
from PIL import Image

dataset = []
data_features = ['Image', 'Namepath', 'Caption', 'Tags']


with gr.Blocks(css='./style.css') as demo:

    gr.Markdown("<h1>TagManagement</h1>")
    message_log = gr.Text(interactive=False, lines=5, show_label=False)

    with gr.Row():
        image_files = gr.Gallery(file_types=['image'], visible=False)

        col1, col2 = gr.Column(scale=1), gr.Column(scale=4)

        def update_message(message_log):
            message_log += '!!!!!!!'
            return message_log
        
        def upload_image(images):
            im_names = [img.name for img in images]
            message_log = message_log + f'Loaded {len(images)} images\n'
            return message_log, im_names
            
        with col1:
            browse_dir = gr.UploadButton(
                label="Open Directory", 
                file_types=['image'],
                file_count='multiple',
                )
            
    x = gr.State([])
    def show_dataset(images):
        dataset_view = []
        
        for i in images:
            print(i)
            with gr.Row():
                with gr.Column(scale=1, min_width=60):
                    img = gr.Image(i, elem_classes='dataview_image')
                with gr.Column(scale=9):
                    with gr.Row():
                        dummy_text = 'arkdown("<h3>Run Auto-captioning</h3>'
                        path = gr.Textbox(dummy_text, show_label=False, elem_classes='dataview_text')
                        capt = gr.Textbox(dummy_text, show_label=False, elem_classes='dataview_text')
                        tags = gr.Textbox(dummy_text, show_label=False, elem_classes='dataview_text')
                yield img, path, capt, tags
                # dataset_view.extend([img, path, capt, tags])
            # dataset_view.extend([img])
        # return dataset_view

    browse_dir.upload(
            show_dataset,
            inputs = [browse_dir], 
            outputs = ['image', 'text', 'text', 'text']
        )
    
    
    # gr.Markdown("<h3>Run Auto-captioning</h3>")
    # with gr.Row():
    #     with gr.Column(scale="3"):
    #         auto_caption_method = gr.Radio(
    #             label="Method", 
    #             choices=['BLIP', 'WaifuDiffusion'],
    #             value='BLIP')
        
    #     with gr.Column(scale="1"):
    #         gr.Button("Run")

    # gr.Markdown("<h3>Dataset</h3>")
    # with gr.Row():
    #     with gr.Column(scale=2):
    #         dataview = gr.DataFrame(
    #             headers=data_features, 
    #             label="Dataset", 
    #             max_rows=20,
    #             col_count=(4, 'fixed'),
    #             interactive=True,
    #             overflow_row_behaviour='paginate',
    #             show_label=False
    #             )
    #     with gr.components.Column(scale=1):
    #         s_choices = gr.State(["girl", "realistic"])
    #         s_values = gr.State(["girl", "realistic"])
            
    #         image_editing = gr.Image(interactive=False)
    #         image_editing_caption = gr.TextArea(
    #             label = 'Caption',
    #             lines=3
    #             )
    #         image_editing_tags = gr.CheckboxGroup(
    #             label="Add tag (Enter to add)",
    #             choices=s_choices.value,
    #             value=s_values.value,
    #             interactive=True
    #         )

    #         new_tag = gr.Textbox(
    #             label="Add tag (Enter to add)"
    #         )

    #         def append_tag(choices, values, newtag):
    #             return choices + [newtag], values + [newtag]
            
    #         def update_tag_ui(s_choices, s_values):
    #             return gr.update(choices=s_choices, value=s_values), gr.update(value="")
            
    #         new_tag.submit(
    #             append_tag, 
    #             inputs=[s_choices, s_values, new_tag],
    #             outputs=[s_choices, s_values]).then(
    #                 update_tag_ui,
    #                 inputs = [s_choices, s_values],
    #                 outputs = [image_editing_tags, new_tag]
    #             )
            
    #         with gr.Row():
    #             save_edition = gr.Button(value="Submit", variant="primary")
    #             reset_edition = gr.Button(value="Reset", variant='secondary')
    
    # with gr.Row():
    #     with gr.Column(scale=1):
    #         save_btn = gr.Button("Save")
    #     with gr.Column(scale=1):
    #         cancel_btn = gr.Button("Cancel")



demo.launch(debug=True)
