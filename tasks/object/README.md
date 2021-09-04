# VoxelScape for 3D Object Detection Task
In our 3D object detction task we relied on the Open3D-ML framework for training/evaluating the PointPillars models in our paper.

Open3D-ML is an extension of Open3D for 3D machine learning tasks.
It builds on top of the Open3D core library and extends it with machine learning
tools for 3D data processing. This repo focuses on applications such as semantic
point cloud segmentation and provides pretrained models that can be applied to
common tasks as well as pipelines for training.

Open3D-ML works with both **TensorFlow** and **PyTorch** but in our experiments we utilised the PyTorch version.

## Installation

### Users

Open3D-ML is integrated in the Open3D v0.11+ python distribution and is
compatible with the following versions of ML frameworks.

 * PyTorch 1.6
 * TensorFlow 2.3
 * CUDA 10.1 (On `GNU/Linux x86_64`, optional)

You can install Open3D with
```bash
# make sure you have the latest pip version
pip install --upgrade pip
# install open3d
pip install open3d
```

To install a compatible version of PyTorch or TensorFlow you can use the
respective requirements files:
```bash
# To install a compatible version of PyTorch with CUDA
pip install -r requirements-torch-cuda.txt
```

To test the installation use

```bash
# with PyTorch
$ python -c "import open3d.ml.torch as ml3d"
```

If you need to use different versions of the ML frameworks or CUDA we recommend
to 
[build Open3D from source](http://www.open3d.org/docs/release/compilation.html).


## Launch Training for PointPillars on VoxelScape with PyTorch.
```
python scripts/run_pipeline.py torch -c ml3d/configs/pointpillars_voxelscape.yml --split train --dataset.dataset_path <path-to-dataset> --pipeline ObjectDetection --dataset.use_cache True

```
For further help, run `python scripts/run_pipeline.py --help`.


## Pre-trained Models

- [PointPillars (VoxelScape)](https://studentutsedu-my.sharepoint.com/:u:/g/personal/khaled_aboufarw_uts_edu_au/EQ06mtkv5WVEtt-cH4Nu-_MBC1SpJPt-NNnO2nEFCunmrw?e=a7CnC9)
- [PointPillars (KITTI)](https://studentutsedu-my.sharepoint.com/:u:/g/personal/khaled_aboufarw_uts_edu_au/EWuzYUpwzjhEmgmf-Gb6QVoBDS8enUKHL66SO8ytrjUmEA?e=b39Vgf)
- [PointPillars (KITTI-Aug)](https://storage.googleapis.com/open3d-releases/model-zoo/pointpillars_kitti_202012221652utc.pth)
- [PointPillars (VS-FT)](https://studentutsedu-my.sharepoint.com/:u:/g/personal/khaled_aboufarw_uts_edu_au/EXDVpI9pEVpMk_4pX8_Z65QB9xGJuQy-tqxiHaIXFkhejA?e=D4Xiwa)
