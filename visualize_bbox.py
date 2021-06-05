import os
import argparse
import yaml
import open3d as o3d
from utils.obj_util import load_bbox_from_pkl, get_bbox_color_lut
import numpy as np




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="./visualize_bbox.py")
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
        default="config/bbox-voxelscape.yaml",
        help='Dataset config file for bbox visualization',
    )
    parser.add_argument(
        '--seq', '-s',
        type=str,
        default="00",
        required=False,
        help='The sequence number to be visualized. 00..99'
    )
    parser.add_argument(
        '--bbox_num', '-bn',
        type=int,
        default=10,
        required=False,
        help='The number of bboxs to visualize per frame/scan. To accelerate the visualzer, due to large number of bboxs.'
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
    # load bbox annotation pkl files
    bboxs_path = os.path.join(seq_path, 'bboxs')
    if os.path.isdir(bboxs_path):
        print("Bboxs folder exists! Using labels from %s" % bboxs_path)
    else:
        print("Bboxs folder doesn't exist! Exiting...")
        quit()
    bboxs_data = sorted(os.listdir(bboxs_path))

    lines = [[0, 1], [1, 2],[2, 3],[3, 0], [4, 5], [5, 6], \
                 [6 ,7], [7, 4], [4, 0], [5, 1], [6 ,2], [7, 3]]
    
    # create open3d pcd and line set for bbox
    pcd = o3d.geometry.PointCloud()
    line_set_list = []
    for j in range(args.bbox_num):
        line_set = o3d.geometry.LineSet()
        line_set_list.append(line_set)
    # create and configure the visualizer
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    vis.add_geometry(pcd)
    for ls in line_set_list:
        vis.add_geometry(ls)
    render_option = vis.get_render_option()
    render_option.point_size = 0.8
    to_reset_view_point = True
    # Get bboxs color map dictionary
    bbox_color_lut = get_bbox_color_lut(CFG)

    for i in range(len(pcd_data)):
        scan = np.fromfile(os.path.join(pcd_path, pcd_data[i]), dtype=np.float32)
        scan = scan.reshape((-1, 4))
        pcd.points = o3d.utility.Vector3dVector(scan[:, 0:3])
        print (bboxs_data[i], pcd_data[i])
        obj_bboxs_ls, obj_cls_ls = load_bbox_from_pkl(os.path.join(bboxs_path,bboxs_data[i]))
        # Get the first $args.bbox_num$ bboxs from the annotation pickle file
        for k in range(args.bbox_num):
            bbox_8_vertices = obj_bboxs_ls[k]
            obj_class_name = obj_cls_ls[k]
            line_set_list[k].points = o3d.utility.Vector3dVector(bbox_8_vertices)
            line_set_list[k].lines = o3d.utility.Vector2iVector(lines)
            obj_colors = [bbox_color_lut[obj_class_name] for ix in range(len(lines))]
            line_set_list[k].colors = o3d.utility.Vector3dVector(obj_colors)
        vis.update_geometry(pcd)
        for m in range(args.bbox_num):
            vis.update_geometry(line_set_list[m])
        if to_reset_view_point:
            vis.reset_view_point(True)
            to_reset_view_point = False
        vis.poll_events()
        vis.update_renderer()
    vis.destroy_window()
