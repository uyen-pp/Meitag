import gradio as gr
from itertools import chain

data_features = ['Checked', 'Image', 'Caption', 'Tags']
max_num_samples = 100


def create_sample(data):
    samples = [(sample.name, '', '') for sample in data]
    return samples

def refresh_dataset(*dataset_ui):
    dataset_ui = [gr.update(value=None, visible=False) for _ in dataset_ui]
    return [None] + dataset_ui

def create_blank_dataset_ui():
    """
    TO create a table with fixed number of rows, which will be replacing by uploaded data
    """
    dataset_view = []
    show_table = False
    for _ in range(max_num_samples):
        with gr.Row():
            with gr.Column(scale=1, min_width=1):
                checked = gr.Checkbox(False, label="", visible=show_table, show_label=False, interactive=False)
            with gr.Column(scale=2, min_width=60):
                img = gr.Image(visible=show_table, show_label=False, elem_classes='dataview_image', interactive=False)
            with gr.Column(scale=16):
                with gr.Row():
                    capt = gr.Textbox(visible=show_table, show_label=False, elem_classes='dataview_text')
                    tags = gr.Textbox(visible=show_table, show_label=False, elem_classes='dataview_text')

        dataset_view.extend([checked, img, capt, tags])
    return dataset_view

def add_dataset(new_samples, old_samples):
    """
    Update dataset includes:
      - Update UI
      - Update dataset state
    """
    
    n_old_sample = len(old_samples)
    n_new_sample = len(new_samples)

    if n_old_sample == 0:
        head_padding = []
    else: 
        head_padding = [
            gr.update()
        ] * len(data_features) * n_old_sample

    
    if n_old_sample + n_new_sample > max_num_samples:
        new_image_files = new_samples[0 : max_num_samples-n_old_sample]
        ### Can show message num sample > max_num_sample
    else:
        new_image_files = new_samples

    new_image_files = create_sample(new_image_files)

    # patten: Phan data moi upload
    pattern = [[gr.update(visible=True, show_label=False), 
            gr.update(value=image[0], visible=True),
            gr.update(value=image[1], visible=True),
            gr.update(value=image[2], visible=True)]
            for image in new_image_files]
    
    # padding: Phan khong chua data thuc (Optimize later)
    tail_padding =  [
            gr.update()
        ] * len(data_features) * (max_num_samples-len(new_image_files))
    
    ret = head_padding + list(chain(*pattern)) + tail_padding
    
    all_data = old_samples + new_image_files
    return [all_data] + ret

def renew_dataset(new_samples):
    # Update dataset includes:
    #   - Update UI
    #   - Update dataset state

    n_new_sample = len(new_samples)

    if n_new_sample > max_num_samples:
        image_files = new_samples[0 : max_num_samples]
        ### Can show message num sample > max_num_sample
    else:
        image_files = new_samples

    image_files = create_sample(image_files)

    # patten: Phan data moi upload
    pattern = [[gr.update(visible=True), 
            gr.update(value=image[0], visible=True),
            gr.update(value=image[1], visible=True),
            gr.update(value=image[2], visible=True)]
            for image in image_files]
    
    # padding: Phan khong chua data thuc (Optimize later)
    tail_padding =  [
            gr.update()
        ] * len(data_features) * (max_num_samples-len(image_files))
    # tail_padding =  [None] * len(data_features) * (max_num_samples-len(image_files))
    ret = list(chain(*pattern)) + tail_padding
    
    return [image_files] + ret

def select_all(dataset):
    x = [True] * len(dataset) + [None]*(max_num_samples-len(dataset))
    return x

def unselect_all():
    x = [False] * max_num_samples
    return x

with gr.Blocks(css='/Users/uyen/MeiTag/style.css') as demo:
    dataset_state = gr.State([])

    with gr.Row():
        left, right = gr.Column(scale=2), gr.Column(scale=1)

        with left:
            # Dataview
            with gr.Row(elem_id='datasset_view'):
                table_ui = create_blank_dataset_ui()

            # Actions
            with gr.Row():
                uploaded = gr.UploadButton(
                            label="Open Directory", 
                            file_types=['image'],
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
                save_invidual_img = gr.Button(
                            value="Save Changess", 
                        )
                reset = gr.Button(
                            value="Reset", 
                        )
                download = gr.Button(
                            value="Download Dataset", 
                        )

            uploaded.upload(renew_dataset, 
                            inputs=uploaded, 
                            outputs=[dataset_state]+table_ui,
                        )
            added.upload(add_dataset, 
                        inputs= [added, dataset_state], 
                        outputs = [dataset_state]+table_ui
                    )
            
            reset.click(refresh_dataset, table_ui, [dataset_state] + table_ui)
            
            btn_select_all.click(select_all, 
                                 dataset_state, 
                                 [ele for ele in table_ui if str(ele)=='checkbox']
                                 )
            btn_unselect_all.click(unselect_all, 
                                   None, 
                                   [ele for ele in table_ui if str(ele)=='checkbox'])
        with right:
            with gr.Row():
                editings = gr.Gallery()
            with gr.Row():
                save_all_img = gr.Button(value="Save", variant='primary')
                cancel_editing = gr.Button(value="Cancel")

    with gr.Row():
        gr.Text("End of page")

demo.queue(concurrency_count=8).launch()
