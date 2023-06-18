from itertools import chain
from dataset import ImageDataset
from torch.utils.data import ConcatDataset
import utils
import gradio as gr
from os import path as osp

class State:
    def __init__(self) -> None:
        self.dataset = []
        self.editings = set([]) #List of editing rows indexes
        self.num_samples = 0

    def open_dataset(self, checkboxes, images, captions, taglists):
        self.dataset = ImageDataset(
            checks = checkboxes,
            img_paths = images,
            captions = captions,
            taglists = taglists
        )

        self.num_samples = len(self.dataset)
    
    def add_sample(self, checkboxes, images, captions, taglists):
        """
        Add a list of sample to current dataset
        """
        dataset = ImageDataset(
            checks = checkboxes,
            img_paths = images,
            captions = captions,
            taglists = taglists
        )
        self.dataset = ConcatDataset([self.dataset, dataset])
        self.num_samples = len(self.dataset)

class DataTableUI:
    def __init__(self, max_num_samples=100) -> None:

        self.state = State()

        self.max_samples = max_num_samples
        self.ui_checkboxes, self.ui_images, self.ui_captions, self.ui_taglists = [], [], [], []
        self.ui_editings = None

    @property
    def num_active_samples(self):
        return self.state.num_samples
        
    @property
    def active_ui_checkboxes(self):
        return self.ui_checkboxes[0: self.num_active_samples]
    @property
    def active_ui_images(self):
        return self.ui_images[0: self.num_active_samples]
    @property
    def active_ui_captions(self):
        return self.ui_captions[0: self.num_active_samples]
    @property
    def active_ui_taglists(self):
        return self.ui_taglists[0: self.num_active_samples]
    
    def init_view(self):
        """
        TO create a table with fixed number of rows, which will be replacing by uploaded data
        """
        # dataset_view = []
        checkboxes = []
        images = []
        captions = []
        taglists = []
        show_table = False

        for _ in range(self.max_samples):
            with gr.Row():
                with gr.Column(scale=1, min_width=1):
                    checked = gr.Checkbox(False, label="", visible=show_table, show_label=False, interactive=True)
                with gr.Column(scale=2, min_width=60):
                    img = gr.Image(visible=show_table, show_label=False, elem_classes='dataview_image', interactive=False)
                with gr.Column(scale=16):
                    with gr.Row():
                        capt = gr.Textbox(visible=show_table, show_label=False, elem_classes='dataview_text', interactive=True)
                        tags = gr.Textbox(visible=show_table, show_label=False, elem_classes='dataview_text', interactive=True)

            checkboxes.append(checked)
            images.append(img)
            captions.append(capt)
            taglists.append(tags)

        self.ui_checkboxes = checkboxes
        self.ui_images = images
        self.ui_captions = captions
        self.ui_taglists = taglists
    
    def checkbox_change(self, checked, idx):
        idx = int(idx)
        if checked: 
            self.state.editings.add(idx)
        elif idx in self.state.editings:
            self.state.editings.remove(idx)

        def fn(i):
            return (self.state.dataset[i].image_path, 
                    self.state.dataset[i].caption + ', ' + ' '.join(self.state.dataset[i].tags)
                    )
        ret = [fn(i) for i in self.state.editings]
        return ret

    def caption_change(self, caption, idx):
        idx = int(idx)
        # self.state.d
    
    def select_all(self):
        x = [True] * self.max_samples
        self.state.editings = set(range(self.num_active_samples))
        return x

    def unselect_all(self):
        x = [False] * self.max_samples
        self.state.editings = set([])
        return x
    
    def create_gallery(self):
        editings = gr.Gallery(interactive = True)
        self.ui_editings = editings

    def update_gallery(self):
        def fn(i):
            return (self.state.dataset[i].image_path, 
                    self.state.dataset[i].caption + ', ' + ' '.join(self.state.dataset[i].tags)
                    )
        ret = [fn(i) for i in self.state.editings]
        return ret

    def save_dataset(self):
        import tempfile
        tmpdir = tempfile.mkdtemp(dir='./tmp')
        path=tmpdir+'/dataset.zip'
        self.state.dataset.zip(path=path)
        return path
        
    def open_dataset(self, files, load_captions:bool, file_extension: str):
        """
        Upload files in chosen dictionary.
                Update dataset including:
                - Update UI
                - Update dataset state
                Files should be image file or caption file. Image file and corresponding caption file must have the same basename.
                Example: image_1.png and image_1.caption
                return Tuple(List[image_files], List[caption_file])
        """

        # create dataset
        files = [f.name for f in files]

        # images_orig = [oname for oname, tname in files if utils.check_image(oname)]
        images = [tname for tname in files if utils.check_image(tname)]

        # Only keep top `max_sample` images 
        if len(images) > self.max_samples:
            images = images[0:self.max_samples]

        captions = [''] * len(images)

        if load_captions:
            for i, img_file in enumerate(images):
                base_name = osp.basename(img_file).rsplit('.', 1)[0]
                cap_file = [tname for tname in files if tname.endswith(base_name+file_extension)]

                if cap_file:
                    with open(cap_file[0]) as s:
                        captions[i] = s.read().strip()
        
        checkboxes = [False] * len(images)
        taglists = [[]] * len(images)

        self.state.open_dataset(checkboxes=checkboxes, images=images, captions=captions, taglists=taglists)

        cb_updates = [gr.update(visible=True)]*len(checkboxes) \
            + [None]*(self.max_samples-len(checkboxes))
        im_updates = [gr.update(visible=True, value=i) for i in images] \
            + [None]*(self.max_samples-len(images))
        cap_updates = [gr.update(visible=True, value=c) for c in captions] \
            + [None]*(self.max_samples-len(captions))
        tag_updates = [gr.update(visible=True, value=l) for l in taglists] \
            + [None]*(self.max_samples-len(taglists))
        
        # Update active row:
        return cb_updates + im_updates + cap_updates + tag_updates

    def add_samples(self, new_samples, load_captions, file_extension):
        print(self.num_active_samples)
        # create dataset
        files = [f.name for f in new_samples]

        # images_orig = [oname for oname, tname in files if utils.check_image(oname)]
        images = [tname for tname in files if utils.check_image(tname)]

        # Only keep top `max_sample` images 
        if len(images) + self.num_active_samples > self.max_samples:
            images = images[0:self.max_samples-self.num_active_samples]

        captions = [None] * len(images)

        if load_captions:
            for i, img_file in enumerate(images):
                base_name = osp.basename(img_file).rsplit('.', 1)[0]
                cap_file = [tname for tname in files if tname.endswith(base_name+file_extension)]

                if cap_file:
                    with open(cap_file[0]) as s:
                        captions[i] = s.read()
        
        checkboxes = [False] * len(images)
        taglists = [[]] * len(images)

        n_current_samples = self.num_active_samples
        n_new_samples = len(images)

        self.state.add_sample(checkboxes, images, captions, taglists)

        cb_updates = [gr.update()] * n_current_samples \
            + [gr.update(visible=True)]*len(checkboxes) \
            + [gr.update()]*(self.max_samples-n_current_samples-n_new_samples)
        
        im_updates = [gr.update()] * n_current_samples \
            + [gr.update(visible=True, value=i) for i in images] \
            + [gr.update()]*(self.max_samples-n_current_samples-n_new_samples)
        
        cap_updates = [gr.update()] * n_current_samples \
            + [gr.update(visible=True, value=c) for c in captions] \
            + [gr.update()]*(self.max_samples-n_current_samples-n_new_samples)
        
        tag_updates = [gr.update()] * n_current_samples \
            + [gr.update(visible=True, value=l) for l in taglists] \
            + [gr.update()]*(self.max_samples-n_current_samples-n_new_samples)
        
        # Update active row:
        return cb_updates + im_updates + cap_updates + tag_updates