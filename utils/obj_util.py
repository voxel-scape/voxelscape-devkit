import numpy as np
import pickle


def load_bbox_from_pkl(pkl_file):
    obj_bboxs = []
    obj_cls = []
    with open(pkl_file, 'rb') as pf:
        annot = pickle.load(pf)
    for i in range(len(annot)):
        obj_bboxs.append(annot[i]['bboxWCWi'])
        obj_cls.append(annot[i]['cls'])
    return obj_bboxs, obj_cls

def get_bbox_color_lut(CFG):
    bbox_color_dict = CFG["color_map"]
    reorder = [2,1,0]
    bbox_color_lut = {}
    for key, value in bbox_color_dict.items():
        bbox_color_lut[key] = np.array(value, np.float32)[reorder,] / 255.0
    return bbox_color_lut
  
