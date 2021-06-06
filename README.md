# API for VoxelScape

This repository contains helper scripts to open, visualize and process point clouds and annotations from the VoxelScape dataset.

- Link to [VoxelScape dataset](https://voxel-scape.github.io/dataset/).
---

## Dataset structure

After downloading and un-zipping each sequence folder from the above download link into `/VoxelScape/dataset/` directory. The data should be organized as follows:

```
/VoxelScape/dataset/
          ├── 00/
          │   ├── bboxs/
          │   │     ├ xyz_iom_000000.pkl
          │   │     └ xyz_iom_000001.pkl
          │   ├── kitti_labels/
          │   │     ├ xyz_iom_000000.label
          │   │     └ xyz_iom_000001.label
          |   ├── orig_labels/
          |   |     ├ xyz_iom_000000_subl.label
          |   |     ├ xyz_iom_000000.label
          |   |     ├ xyz_iom_000001_subl.label
          |   |     ├ xyz_iom_000001.label
          │   └── velodyne/
          │         ├ xyz_iom_000000.bin
          │         └ xyz_iom_000001.bin
          ├── 01/
          ├── 02/
          .
          .
          .
          └── 99/
```
- `velodyne` contains the pointclouds for each scan in each sequence. Each 
`.bin` scan is a list of float32 points in [x,y,z,remission] format.
- `bboxs` contains the 3D bounding boxes annotation of the 9 object classes in the dataset. Each `.pkl` 
file contains the 8-vertices of the 3D bounding box and classs labels for each object exist in the corresponding `.bin` scan.
- `kitti_labels` contains only 19 merged/subset semantic class labels, which correspond to the labels exist in the SemanticKITTI dataset, for each scan in each sequence. Each `.label` file contains a uint32 label for each point in the corresponding `.bin` scan.
- `orig_labels` contains the total 32 semantic class labels introduced in the VoxelScape dataset. Each `_subl.label` file contains a fine-grained uint32 label for differnet attributes of each object in the corresponding `.bin` scan. See [sem_util.py](utils/sem_util.py) for more information on the sub-labels.

The dataset has two main configuration files, namely `config/semantic-voxelscape.yaml` and `config/bbox-voxelscape.yaml`. As the name implies, the first config file corresponds to the semantic labels, while the second one corresponds to the 3D bbox annotations. There's also another config file `config/semantic-kitti.yaml` which has the semantic class labels from the SemanticKITTI dataset which can be used for visualising only the 19 subset labels from `kitti_labels`. In both the `config/semantic-voxelscape.yaml` and `config/semantic-kitti.yaml` files you will find:

- `labels`: dictionary which maps the numeric labels in `_subl.label/.label` files inside `orig_labels/kitti_labels` folder to a string class. Example: `256: "construction-cone"`
- `color_map`: dictionary which maps numeric labels in `_subl.label/.label` files inside `orig_labels/kitti_labels` folder to a bgr color for visualization. Example `256: [79, 79, 47] # construction-cone, dark green-ish`

## Dependencies for API:

System dependencies

```sh
$ sudo apt install python3-dev python3-pip
```

Python dependencies

```sh
$ sudo pip3 install -r requirements.txt
```

## Scripts:

**ALL OF THE SCRIPTS CAN BE INVOKED WITH THE --help (-h) FLAG, FOR EXTRA INFORMATION AND OPTIONS.**

#### Semantic Labels 

To visualize the full 32 semantic labels of the VoxelScape dataset, use the `visualize_semantic.py` script. It will open an interactive
open3d visualization of the pointclouds

```sh
$ ./visualize_semantic.py --dataset /path/to/voxelscape/dataset/ --seq 00
```

where:
- `dataset` is the path to the VoxelScape dataset.
- `seq` is the sequence folder to be accessed.

In order to visualize only the 19 subset semantic labels (similar to the SemanticKITTI dataset) instead, pass the SemanticKITTI configuration file `config/semantic-kitti.yaml` to the `--config` option:

```sh
$ ./visualize_semantic.py --dataset /path/to/voxelscape/dataset/ --seq 00  --config config/semantic-kitti.yaml
```

#### 3D Bbox Labels

To visualize the data, use the `visualize_voxels.py` script. It will open an interactive
opengl visualization of the voxel grids and options to visualize the provided voxelizations 
of the LiDAR data.

```sh
$ ./visualize_bbox.py --dataset /path/to/voxelscape/dataset/ --seq 00 
```

where:
- `dataset` is the path to the VoxelScape dataset.
- `seq` is the sequence folder to be accessed.

In order to accelerate the visualization, the maximum number of 3D bboxs rendered for each frame is limited to 10 3D bbox per each scan. You can change this number by changing the `--bbox_num` option :

```sh
$ ./visualize_semantic.py --dataset /path/to/voxelscape/dataset/ --seq 00  --bbox_num 15
```
