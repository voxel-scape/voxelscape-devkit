import numpy as np
import os, argparse, pickle, sys
from os.path import exists, join, isfile, dirname, abspath, split
from pathlib import Path
from glob import glob
import logging
import yaml

from .base_dataset import BaseDataset, BaseDatasetSplit
from ..utils import Config, make_dir, DATASET
from .utils import DataProcessing, BEVBox3D

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(asctime)s - %(module)s - %(message)s',
)
log = logging.getLogger(__name__)


class VScape(BaseDataset):
    """
    VoxelScape dataset for Object Detection, used in visualizer, training, or test
    """

    def __init__(self,
                 dataset_path,
                 name='VScape',
                 cache_dir='./logs/cache',
                 use_cache=False,
                 val_split=3712,
                 **kwargs):
        """
        Initialize
        Args:
            dataset_path (str): path to the dataset
            kwargs:
        """
        super().__init__(dataset_path=dataset_path,
                         name=name,
                         cache_dir=cache_dir,
                         use_cache=use_cache,
                         val_split=val_split,
                         **kwargs)

        cfg = self.cfg

        self.name = cfg.name
        self.dataset_path = cfg.dataset_path
        self.num_classes = 3
        skip_frames = 5
        self.label_to_names = self.get_label_to_names()
        self.all_files = []
        self.train_files = []
        self.val_files = []
        
        root = os.path.join(self.dataset_path, "sequences")
        for seq in range(108):
          # to string
          seq = '{0:02d}'.format(seq)
          # get paths for each
          scan_path = os.path.join(root, seq, "velodyne")
          if Path(scan_path).exists() and len(glob(join(scan_path, '*.bin'))) > 0 and '99' not in scan_path:
            print("parsing seq {}".format(seq))
            all_files = sorted(glob(join(scan_path, '*.bin')))
            all_files = [item for index, item in enumerate(all_files) if (index) % skip_frames == 0]
            self.all_files.extend(all_files)
        
        self.train_files = self.all_files[:-1000]
        self.val_files = self.all_files[-1000:]
        self.test_files = glob(
            join(root, '99', 'velodyne', '*.bin'))

    @staticmethod
    def get_label_to_names():
        label_to_names = {
            0: 'Pedestrian',
            1: 'Cyclist',
            2: 'Car',
            3: 'Truck',
            4: 'Bus',
            5: 'Motorcyclist',
            6: 'Kid',
            7: 'Cone',
            8: 'Barrier'
        }
        return label_to_names

    @staticmethod
    def read_lidar(path):
        assert Path(path).exists()

        return np.fromfile(path, dtype=np.float32).reshape(-1, 4)

    @staticmethod
    def read_label(path):
        if not Path(path).exists():
            return []

        with open(path, 'r') as f:
            lines = f.readlines()

        objects = []
        for line in lines:
            # label = line.strip().split(' ')

            # center = np.array(
            #     [float(label[11]),
            #      float(label[12]),
            #      float(label[13]), 1.0])

            # points = center @ np.linalg.inv(calib['world_cam'])

            # size = [float(label[9]), float(label[8]), float(label[10])]  # w,h,l
            # center = [points[0], points[1], size[1] / 2 + points[2]]

            objects.append(Object3d(line))#center, size, label, calib))

        return objects

    @staticmethod
    def _extend_matrix(mat):
        mat = np.concatenate([mat, np.array([[0., 0., 0., 1.]])], axis=0)
        return mat

    def get_split(self, split):
        return VScapeSplit(self, split=split)

    def get_split_list(self, split):
        cfg = self.cfg
        dataset_path = cfg.dataset_path
        file_list = []

        if split in ['train', 'training']:
            return self.train_files
            seq_list = cfg.training_split
        elif split in ['test', 'testing']:
            return self.test_files
        elif split in ['val', 'validation']:
            return self.val_files
        elif split in ['all']:
            return self.train_files + self.val_files + self.test_files
        else:
            raise ValueError("Invalid split {}".format(split))

    def is_tested(self):
        pass

    def save_test_result(self):
        pass


class VScapeSplit():

    def __init__(self, dataset, split='train'):
        self.cfg = dataset.cfg
        path_list = dataset.get_split_list(split)
        log.info("Found {} pointclouds for {}".format(len(path_list), split))

        self.path_list = path_list
        self.split = split
        self.dataset = dataset

    def __len__(self):
        return len(self.path_list)

    def get_data(self, idx):
        pc_path = self.path_list[idx]
        label_path = pc_path.replace('velodyne',
                                     'bboxs').replace('.bin', '.txt')

        pc = self.dataset.read_lidar(pc_path)
        label = self.dataset.read_label(label_path)

        # reduced_pc = DataProcessing.remove_outside_points(
        #     pc, calib['world_cam'], calib['cam_img'], [370, 1224])

        data = {
            'point': pc,
            'feat': None,
            'calib': None,
            'bounding_boxes': label,
        }

        return data

    def get_attr(self, idx):
        pc_path = self.path_list[idx]
        name = str(Path(pc_path).parents[1]).split('/')[-1]+'_'+Path(pc_path).name.split('.')[0]

        attr = {'name': name, 'path': pc_path, 'split': self.split}
        return attr


def cls_type_to_id(cls_type):
    type_to_id = {'Car': 2, 'Pedestrian': 0, 'Cyclist': 1, 'Truck': 3, 'Motorcyclist': 5, 'Bus': 4, 'Kid': 6, 'Cone': 7, 'Barrier': 8}
    if cls_type not in type_to_id.keys():
        return -1
    return type_to_id[cls_type]


class Object3d(BEVBox3D):
    def __init__(self, line):
        label = line.strip().split(' ')
        
        confidence = -1
        world_cam = None#calib['world_cam']
        cam_img = None#calib['cam_img']
        
        yaw = float(label[7]) - np.pi
        yaw = yaw - np.floor(yaw / (2 * np.pi) + 0.5) * 2 * np.pi
        class_name = label[0] if label[0] in VScape.get_label_to_names().values(
        ) else 'DontCare'
        self.truncation = 0#float(label[1])
        self.occlusion = 0#float(label[2])  # 0:fully visible 1:partly occluded 2:largely occluded 3:unknown
        self.alpha = -0.2#float(label[3])
        h = float(label[1])
        w = float(label[2])
        l = float(label[3])
        center = [float(label[4]), float(label[5]), float(label[6])+(h/2.0)]
        super().__init__(center, [w, h, l], yaw, class_name, confidence, world_cam,
                         cam_img)
        self.yaw = yaw#float(label[7])
        self.score = -1#float(label[15]) if label.__len__() == 16 else -1.0
        self.level_str = None
        self.level = 0#self.get_kitti_obj_level()
        self.num_points_in_gt = int(label[8])



DATASET._register_module(VScape)
