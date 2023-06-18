import gradio as gr
from state import DataTableUI, State
import utils
from os import path as osp

max_num_samples = 500

def create_sample(data):
    samples = [(sample.name, '', '') for sample in data]
    return samples

def refresh_dataset(*dataset_ui):
    dataset_ui = [gr.update(value=None, visible=False) for _ in dataset_ui]
    return [None] + dataset_ui


with gr.Blocks(css='/Users/uyen/MeiTag/style.css') as demo:

    with gr.Row():
        left, right = gr.Column(scale=2), gr.Column(scale=1)

        with left:
            # Dataviewx
            with gr.Row(elem_id='dataset_view'):
                table_ui = DataTableUI(100)

            with gr.Row():
                with gr.Column():
                    capt_ext = gr.Textbox(value='.caption', label='Caption file extension:', interactive=True)
                with gr.Column():
                    load_capt = gr.Checkbox(label='Load existing captions', value=True)

            # Actions
            with gr.Row():
                uploaded = gr.UploadButton(
                            label="Open Directory", 
                            file_count='directory'
                            )
                
                added = gr.UploadButton(
                            label="Add Samples", 
                            file_types=['image'],
                            file_count='multiple',
                        )
                btn_select_all = gr.Button(
                            value="Select All", 
                        )
                btn_unselect_all = gr.Button(
                            value="Unselect All"
                            )
                btn_save_invidual_imgs = gr.Button(
                            value="Save Changes", 
                        )
                reset = gr.Button(
                            value="Reset", 
                        )
                download = gr.Button(
                            value="Download Dataset", 
                        )
            
            uploaded.upload(table_ui.open_dataset,
                            inputs = [uploaded, load_capt, capt_ext],
                            outputs = table_ui.ui_checkboxes \
                                + table_ui.ui_images \
                                + table_ui.ui_captions \
                                + table_ui.ui_taglists
                    )
            
            added.upload(table_ui.add_samples, 
                        inputs= [added, load_capt, capt_ext], 
                        outputs = table_ui.ui_checkboxes[table_ui.num_active_samples::]\
                                + table_ui.ui_images[table_ui.num_active_samples::] \
                                + table_ui.ui_captions[table_ui.num_active_samples::] \
                                + table_ui.ui_taglists[table_ui.num_active_samples::]
                    )
            
            # reset.click(refresh_dataset, table_ui, [dataset_state] + table_ui)
            
            btn_select_all.click(table_ui.select_all, 
                                 outputs=table_ui.ui_checkboxes
                                 )
            btn_unselect_all.click(table_ui.unselect_all, 
                                   outputs=table_ui.ui_checkboxes)
            
            # btn_save_invidual_imgs.click(save, table_ui, dataset_state)
        with right:
            with gr.Row():
                editings = gr.Gallery()
            with gr.Row():
                save_all_img = gr.Button(value="Save", variant='primary')
                cancel_editing = gr.Button(value="Cancel")

    with gr.Row():
        gr.Text("End of page")

if __name__ == "__main__":
    demo.queue(concurrency_count=16).launch()
