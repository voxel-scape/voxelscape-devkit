import numpy as np
import yaml

def get_labels(labels_file, sub_labels_file=None):

    labels = np.fromfile(labels_file, dtype=np.int32)
    labels = labels.reshape((-1))

    if sub_labels_file is not None:
        sub_labels = np.fromfile(sub_labels_file, dtype=np.int32)
        sub_labels = sub_labels.reshape((-1))

        if len(labels) != len(sub_labels):
            print ('No of labels and sub-labels is not similar!')
            quit()

        labels[labels==11] = 10  #car
        labels[labels==17] = 10  #car
        labels[labels==18] = 10  #car
        labels[labels==19] = 10  #car
        labels[labels==15] = 11  #bicycle - frame
        labels[sub_labels==151] = 11  #bicycle - frame
        labels[sub_labels==152] = 11  #bicycle - wheels
        labels[labels==13] = 18  #truck
        labels[labels==12] = 13  #bus
        labels[labels==14] = 15  #motorcycle
        labels[sub_labels==141] = 15  #bicycle - frame
        labels[sub_labels==142] = 15  #bicycle - wheels
        labels[labels==69] = 80  #pole
        labels[sub_labels==694] = 80  #pole
        labels[labels==61] = 99  # props-pot
        labels[sub_labels==61] = 99  # props-pot
        labels[labels==60] = 253   #other-object - seat
        labels[sub_labels==60] = 253  #other-object - seat
        labels[sub_labels==424] = 60  #lane-marking - middle-line
        labels[sub_labels==425] = 60  #lane-marking - boundary lines
        labels[sub_labels==426] = 49  #lane-marking - crosswalk
        labels[sub_labels==427] = 49  #lane-marking - cross lines
        labels[sub_labels==428] = 49  #lane-marking - cross lines
        labels[sub_labels==429] = 49  #lane-marking - cross lines
        labels[labels==30] = 50  #building
        labels[labels==31] = 50  #building
        labels[labels==32] = 50  #building
        labels[labels==33] = 50  #building
        labels[labels==34] = 50  #building
        labels[labels==21] = 30  #adult
        labels[sub_labels==21] = 30  #adult
        labels[labels==24] = 16  #ped - kids
        labels[sub_labels==24] = 16  #ped - kids
        labels[labels==23] = 31  #bycyclist
        labels[sub_labels==23] = 31  #bycyclist
        labels[labels==22] = 32  #motorcyclist
        labels[sub_labels==22] = 32  #motorcyclist
        labels[sub_labels==421] = 40  #road
        #labels[sub_labels==425] = 40  #road
        labels[sub_labels==431] = 40  #road
        labels[sub_labels==423] = 20  #curb
        labels[labels==46] = 44  #parking
        labels[sub_labels==441] = 44  #parking - asphalt
        labels[sub_labels==442] = 44  #parking - lines
        labels[sub_labels==422] = 48  #sidewalk
        labels[sub_labels==642] = 51  #Fences
        labels[labels==62] = 52  #other-structure - phone booth
        labels[sub_labels==62] = 52  #other-structure - phone booth
        labels[labels==68] = 52  #other-structure - phone booth
        labels[sub_labels==68] = 52  #other-structure - phone booth
        labels[labels==63] = 252  #other-structure - bus stop
        labels[sub_labels==63] = 252  #other-structure - bus stop
        labels[labels==67] = 258  #other-structure - firehydrant
        labels[sub_labels==67] = 258  #other-structure - firehydrant
        labels[labels==65] = 254  #other-object - mailbox
        labels[sub_labels==65] = 254  #other-object - mailbox
        labels[sub_labels==641] = 255  #other-structure - construction-barrier
        labels[sub_labels==643] = 256  #other-structure - construction-cone
        labels[sub_labels==912] = 70  #vegetation
        labels[labels==92] = 70  #vegetation
        labels[sub_labels==921] = 70  #vegetation
        labels[sub_labels==93] = 72  #terrain - grass
        labels[labels==93] = 72  #terrain - grass
        labels[labels==41] = 72  #terrain - grass
        labels[sub_labels==411] = 72  #terrain - grass
        labels[sub_labels==412] = 72  #terrain - grass
        labels[sub_labels==911] = 71  #trunk
        labels[sub_labels==691] = 81  #traffic-sign - street sign
        labels[sub_labels==692] = 257  #traffic-sign - trafic light
        labels[sub_labels==693] = 257  #traffic-sign - crossing light
        labels[labels==66] = 259  #other-object - trashcan
        labels[sub_labels==66] = 259  #other-object - trashcan
    return labels


def get_sem_color_lut(CFG):
    sem_color_dict = CFG["color_map"]
    max_sem_key = 0
    reorder = [2,1,0]
    for key, data in sem_color_dict.items():
        if key + 1 > max_sem_key:
            max_sem_key = key + 1
    sem_color_lut = np.zeros((max_sem_key + 100, 3), dtype=np.float32)
    for key, value in sem_color_dict.items():
        sem_color_lut[key] = np.array(value, np.float32)[reorder,] / 255.0
    return sem_color_lut


def get_sem_color_labels(CFG, labels):
    
    sem_color_lut = get_sem_color_lut(CFG)
    sem_label_color = sem_color_lut[labels]
    sem_label_color = sem_label_color.reshape((-1, 3))
    return sem_label_color
  
