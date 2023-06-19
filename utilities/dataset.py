
# from torchvision.io import read_image
from dataclasses import dataclass
from zipfile import ZipFile
from os import path as osp

@dataclass
class DataRow:
    checked: bool
    image_path: str 
    caption: str
    tags: list

    def check(self):
        self.checked = True

    def uncheck(self):
        self.checked = False

class ImageDataset:
    def __init__(self, checks, img_paths, captions, taglists):
        self.all = [
            DataRow(ch, i, c, t) for ch, i, c, t in zip(checks, img_paths, captions, taglists)
            ]

    @property
    def checks(self):
        return [sample.checked for sample in self.all]
    
    @property
    def img_paths(self):
        return [sample.image_path for sample in self.all]
    
    @property
    def captions(self):
        return [sample.caption for sample in self.all]
    
    @property
    def taglists(self):
        return [sample.tags for sample in self.all] 

    def __getitem__(self, idx):
        return self.all[idx]
    
    def __len__(self):
        return len(self.checks)
    
    def zip(self, path, caption_extension='.caption'):
        zipobj = ZipFile(path, 'w')

        for item in self.all:

            caption_fname = osp.basename(item.image_path).rsplit('.', 1)[0] + caption_extension
            image_fname = osp.basename(item.image_path)

            caption = ', '.join([item.caption.strip()] + item.tags)

            zipobj.write(filename=item.image_path, arcname=image_fname)
            zipobj.writestr(caption_fname, data=caption)

# Test
if __name__ == "__main__":
    chbxes = [False] * 10
    imgs = ['image.com'] * 10
    caps = ['dummy examples'] * 10
    tags = [['tag1', 'tag 2']] * 10
    dataset = ImageDataset(chbxes, imgs, caps, tags)

    print(dataset[3])
    print(len(dataset))
    print(dataset.captions)

    dataset[3].image_path = 'changed_image_path.png'
    print(dataset[3])