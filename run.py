import gradio as gr
from state import DataTableUI, State
import utils
from os import path as osp

max_num_samples = 10
UI = DataTableUI(max_num_samples)

with gr.Blocks(css='./style.css') as demo:

    gr.Markdown("<h1>TagManagement</h1>")
    
    with gr.Row():
        left, right = gr.Column(scale=2), gr.Column(scale=1)

        with left:
            # Dataviewx
            with gr.Row(elem_id='dataset_view'):
                UI.init_view()
            with gr.Row():
                with gr.Column():
                    capt_ext = gr.Textbox(value='.caption', label='Caption file extension:', interactive=True)
                with gr.Column():
                    load_capt = gr.Checkbox(label='Load existing captions', value=True)
            with gr.Row():
                progress=gr.Progress()
            # Actions
            with gr.Row():
                uploaded = gr.UploadButton(
                            label="Open Directory", 
                            file_count='directory', 
                            variant='primary',
                        )
                added = gr.UploadButton(
                            label="Add Samples", 
                            file_count='multiple',
                        )
                btn_select_all = gr.Button(
                            value="Select All", 
                        )
                btn_unselect_all = gr.Button(
                            value="Unselect All"
                        )
                btn_save = gr.Button(
                            value="Save Changes", 
                        )
                dataset_zip = gr.File(show_label=False, elem_id='dataset_download')
   
        with right:
            with gr.Row():
                UI.create_gallery()
            with gr.Row():
                with gr.Column():
                    prefix = gr.Textbox(label="Add pre-fix")
                    suffix = gr.Textbox(label="Add suffix")
                    tags = gr.Textbox(label="Add tags")
            with gr.Row():
                save_all_img = gr.Button(value="Save", variant='primary')
                cancel_editing = gr.Button(value="Cancel")
            with gr.Row():
                message_log = gr.Text(interactive=False, lines=5, show_label=False)

        uploaded.upload(UI.open_dataset,
                            inputs = [uploaded, load_capt, capt_ext],
                            outputs = UI.ui_checkboxes \
                                + UI.ui_images \
                                + UI.ui_captions \
                                + UI.ui_taglists
                    )
            
        added.upload(UI.add_samples, 
                    inputs= [added, load_capt, capt_ext], 
                    outputs = UI.ui_checkboxes\
                            + UI.ui_images \
                            + UI.ui_captions\
                            + UI.ui_taglists
                )
        
        for idx, ch in enumerate(UI.ui_checkboxes):
            ch.input(UI.checkbox_change, inputs=[ch, gr.Number(idx, visible=False)], outputs=UI.ui_editings)

        btn_select_all.click(UI.select_all, 
                        outputs= UI.ui_checkboxes
                        ).then(
                            UI.update_gallery, 
                            outputs=UI.ui_editings
                            )
        
        btn_unselect_all.click(UI.unselect_all, 
                        outputs=UI.ui_checkboxes
                        ).then(
                            UI.update_gallery, 
                            outputs=UI.ui_editings
                            )
        
        btn_save.click(UI.save_dataset, outputs=dataset_zip)


if __name__ == "__main__":
    demo.queue(concurrency_count=16).launch()
