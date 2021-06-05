import os
import argparse
import yaml
import open3d as o3d
from utils.sem_util import get_labels, get_sem_color_labels
import numpy as np




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="./visualize_semantic.py")
    parser.add_argument(
        '--dataset', '-d',
        type=str,
        required=True,
        help='Path to the parent directory of VoxelScape dataset. No Default',
    )
    parser.add_argument(
        '--config', '-c',
        type=str,
        required=False,
        default="config/semantic-voxelscape.yaml",
        help='Dataset config file. Either visualize full VoxelScape labels or kitti-subset labels',
    )
    parser.add_argument(
        '--seq', '-s',
        type=str,
        default="00",
        required=False,
        help='The sequence number to be visualized. 00..99'
    )
    args = parser.parse_args()

    # open config file
    try:
        print("Opening config file %s" % args.config)
        CFG = yaml.safe_load(open(args.config, 'r'))
    except Exception as e:
        print(e)
        print("Error opening yaml file.")
        quit()
    # open check sequence and point cloud folders exist
    seq_path = os.path.join(args.dataset, args.seq)
    if os.path.isdir(seq_path):
        print("Sequence folder exists! Using sequence from %s" % seq_path)
    else:
        print("Sequence folder doesn't exist! Exiting...")
        quit()
    
    pcd_path = os.path.join(seq_path,'velodyne')
    if os.path.isdir(pcd_path):
        print("PCD folder exists! Using PCD from %s" % pcd_path)
    else:
        print("PCD folder doesn't exist! Exiting...")
        quit()
    pcd_data = sorted(os.listdir(pcd_path))
    # Either visualize sequence using full labels or the subset kitti labels
    if 'kitti' in args.config:
        labels_path = os.path.join(seq_path, 'kitti_labels')
        if os.path.isdir(labels_path):
            print("Labels folder exists! Using labels from %s" % labels_path)
        else:
            print("Labels folder doesn't exist! Exiting...")
            quit()
        labels_data = sorted(os.listdir(labels_path))
    else:
        labels_path = os.path.join(seq_path, 'orig_labels')
        if os.path.isdir(labels_path):
            print("Labels folder exists! Using labels from %s" % labels_path)
        else:
            print("Labels folder doesn't exist! Exiting...")
            quit()
        all_label_files = os.listdir(labels_path)
        sub_labels_data = [fl for fl in all_label_files if fl.endswith('_subl.label')]
        sub_labels_data = sorted(sub_labels_data)
        labels_data = [fl for fl in all_label_files if fl.endswith('.label') and fl not in sub_labels_data]
        labels_data = sorted(labels_data)

    # create open3d pcd
    pcd = o3d.geometry.PointCloud()
    # create and configure the visualizer
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    vis.add_geometry(pcd)
    render_option = vis.get_render_option()
    render_option.point_size = 0.8
    to_reset_view_point = True

    for i in range(len(pcd_data)):
        scan = np.fromfile(os.path.join(pcd_path, pcd_data[i]), dtype=np.float32)
        scan = scan.reshape((-1, 4))
        pcd.points = o3d.utility.Vector3dVector(scan[:, 0:3])
        print (labels_data[i], pcd_data[i])
        if 'kitti' in args.config:
            labels = get_labels(os.path.join(labels_path,labels_data[i]))
        else:
            labels = get_labels(os.path.join(labels_path,labels_data[i]), os.path.join(labels_path, sub_labels_data[i]))
        sem_label_color = get_sem_color_labels(CFG, labels)
        pcd.colors = o3d.utility.Vector3dVector()
        pcd.colors = o3d.utility.Vector3dVector(sem_label_color)
        vis.update_geometry(pcd)
        if to_reset_view_point:
            vis.reset_view_point(True)
            to_reset_view_point = False
        vis.poll_events()
        vis.update_renderer()
    vis.destroy_window()
