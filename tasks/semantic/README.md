# VoxelScape for Point-wise Semantic Segmentation Task
In our point-wise semantic segmentation task we relied on both [LiDAR-Bonnetal](https://github.com/PRBonn/lidar-bonnetal)
and [Open3D-ML](https://github.com/isl-org/Open3D-ML) framework for training/evaluating the projection-based DNN models (i.e. SqueezeSeqV2 and Darknet53) and point-based DNN model (i.e. RandLANet) in our paper.

## Projection-based DNN Models

### Training
To train a network on our VoxelScape dataset with the full original labels from scratch:

```sh
$ ./train.py -d /path/to/dataset -ac config/arch/CHOICE.yaml -dc config/labels/semantic-VoxelScape-all.yaml -l /path/to/log
```
### Inference

To infer the predictions for the entire dataset:

```sh
$ ./infer.py -d /path/to/dataset/ -l /path/for/predictions -m /path/to/model
````

### Evaluation

To evaluate the overall IoU of the point clouds (of a specific split, which in semantic kitti can only be train and valid, since test is only run in our evaluation server):

```sh
$ ./evaluate_iou.py -d /path/to/dataset -p /path/to/predictions/ --split valid
```

## Point-based DNN Model

### Training 
```
cd ../object/
python scripts/run_pipeline.py torch -c ml3d/configs/randlanet_voxelscape.yml --split train --dataset.dataset_path <path-to-dataset> --pipeline SemanticSegmentation --dataset.use_cache True

```
For further help, run `python scripts/run_pipeline.py --help`.

### Inference and Evaluation 
```
cd ../object/
python scripts/run_pipeline.py torch -c ml3d/configs/randlanet_voxelscape.yml --split test --dataset.dataset_path <path-to-dataset> --pipeline SemanticSegmentation --dataset.use_cache True

```
For further help, run `python scripts/run_pipeline.py --help`.

## Pre-trained Models

### Intensity Evaluation Experiment

- [SqueezeSeqV2(-INT)](https://studentutsedu-my.sharepoint.com/:u:/g/personal/khaled_aboufarw_uts_edu_au/EZK-mL9J0jNJo4WhmA_m9S8BaZjUdLLq45fjnANJqaxzZw?e=LRrf25)
- [SqueezeSeqV2(+INT)](https://studentutsedu-my.sharepoint.com/:u:/g/personal/khaled_aboufarw_uts_edu_au/EYt8qkZhG2JGjlNWLruMx38BBmhLjz9yNKpGKkFzkMeTwQ?e=YdlaTz)
- [Darknet53(-INT)](https://studentutsedu-my.sharepoint.com/:u:/g/personal/khaled_aboufarw_uts_edu_au/EWb2WqPabdxKpQ8oLzzqDPMBoYgVDsDvlIGAcUza0BW4pA?e=lJAWBd)
- [Darknet53(+INT)](https://studentutsedu-my.sharepoint.com/:u:/g/personal/khaled_aboufarw_uts_edu_au/EZoo1p6O0TRKkKveceLWmCABbFQjp3DZZPUwDX9aCcOYhQ?e=f7Yjey)
- [RandLANet(-INT)](https://studentutsedu-my.sharepoint.com/:u:/g/personal/khaled_aboufarw_uts_edu_au/EWb2WqPabdxKpQ8oLzzqDPMBoYgVDsDvlIGAcUza0BW4pA?e=lJAWBd)

### Generalisation Evaluation Experiment

- [SqueezeSeqV2](https://studentutsedu-my.sharepoint.com/:u:/g/personal/khaled_aboufarw_uts_edu_au/EQ9KVtTtSeBKj13aFDDULBQBEpnlAxwMBCJ2oYOqBbxKSA?e=VkhqRD)
- [SqueezeSeqV2 (VS-FT)](https://studentutsedu-my.sharepoint.com/:u:/g/personal/khaled_aboufarw_uts_edu_au/EWb2WqPabdxKpQ8oLzzqDPMBoYgVDsDvlIGAcUza0BW4pA?e=q0G6NF)
- [DarkNet53](https://studentutsedu-my.sharepoint.com/:u:/g/personal/khaled_aboufarw_uts_edu_au/EUGXVdCzDSxMkkf0MSyxU5UBxqcUqyUhYolNmcFYNqq3Ow?e=k7Y4q8)
- [DarkNet53 (VS-FT)](https://studentutsedu-my.sharepoint.com/:u:/g/personal/khaled_aboufarw_uts_edu_au/EZgM_ltqBqlDhRqxxGNGiYABXxCPR-Imw5UlgIytALc4uA?e=dOgu6m)
- [RandLANet] (https://storage.googleapis.com/open3d-releases/model-zoo/randlanet_semantickitti_202009090354utc.pth)
- [RandLANet (VS-FT)](https://studentutsedu-my.sharepoint.com/:u:/g/personal/khaled_aboufarw_uts_edu_au/EZgM_ltqBqlDhRqxxGNGiYABXxCPR-Imw5UlgIytALc4uA?e=dOgu6m)
