import os
import numpy as np
import matplotlib.pyplot as plt
import cv2
import random

def show_gt(list_path, image_path, num_classes = 4) :

    color = (random.random(), random.random(), random.random())

    assert os.path.exists(list_path), 'Path does not exist: {}'.format(list_path)
    with open(list_path, 'r') as f:
        for line in f:
            box_list = []
            label = line.strip().split(':')
            image_name = label[0]

            bbox = label[1:]
            for i in range(4):
                if len(bbox[i]) == 0:
                    box_list.append([])
                    continue
                else:
                    class_i_box = map(float, bbox[i].strip().split(' '))
                    box_list.append(class_i_box)              
            
            boxes = np.concatenate([np.array(box_list[i], dtype=np.float32) for i in range(num_classes)], axis=0)
            boxes = boxes.reshape(-1, 12)
            im = cv2.imread( image_path + image_name)
            
            #rotation_y(1), alpha(1), bbox(4), dims(3), location(3), length is 12
            for box in boxes:
                
                rot   = box[0]
                alpha = box[1]
                bbox  = box[2:6]
                dims  = box[6:9]
                locs  = box[9:12]

                rect = plt.Rectangle((bbox[0], bbox[1]),
                                 bbox[2] - bbox[0],
                                 bbox[3] - bbox[1], fill=False,
                                 edgecolor=color, linewidth=3.5)  
                plt.gca().add_patch(rect)                        
                plt.gca().text(bbox[0], bbox[3] - 2,
                           '{:s} {:.3f} {:s} {:.3f} {:.3f} {:.3f} {:s} {:.3f} {:.3f} {:.3f}'.format('rot', rot, 'dims', dims[0], dims[1], dims[2], 'locs', locs[0], locs[1], locs[2]),
                           bbox=dict(facecolor=color, alpha=0.5), fontsize=12, color='white')

            plt.imshow(im)
            plt.show()

if __name__ == '__main__':

    list_path = "data/kitti/imglists/val.lst"    
    image_path = "data/kitti/images/"

    show_gt(list_path, image_path)
