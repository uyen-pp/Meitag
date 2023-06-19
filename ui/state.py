from utilities.dataset import ImageDataset
from torch.utils.data import ConcatDataset

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

