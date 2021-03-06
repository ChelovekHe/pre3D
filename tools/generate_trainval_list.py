import os

def generate(list_path, src_path, save_path) :
    name2id = dict()
    name2id["Car"] = 0
    name2id["Pedestrian"] = 1
    name2id["Cyclist"] = 2
    name2id["DontCare"] = 3
    name2id["Van"] = 3
    name2id["Truck"] = 3
    name2id["Person_sitting"] = 3
    name2id["Tram"] = 3
    name2id["Misc"] = 3    

    save_file = open(save_path, 'w')

    assert os.path.exists(list_path), 'Path does not exist: {}'.format(list_path)
    with open(list_path, 'r') as f:
        for image_name in f:
            image_name = image_name.strip()
            image_split = image_name.strip().split('.')
            annotation_file = os.path.join(src_path, image_split[0] + '.txt')
            assert os.path.exists(annotation_file), 'Path does not exist: {}'.format(annotation_file)

            box_list = [[], [], []]
            is_has_car = False
            with open(annotation_file, 'r') as af:
                for line in af:

                    label = line.strip().split(' ')
                    class_id = name2id[label[0]]
                    bbox = label[2:14]
                    bbox[0] = label[-1]

                    # rotation_y, alpha, bbox, dims, location
                    # get Car only
                    if class_id == 0 :
                           is_has_car = True
                           box_list[class_id].append(bbox)

                    print bbox

            print image_name

            if is_has_car == True:
                save_file.write(image_split[0] + '.png')
                for class_id in xrange(len(box_list)):
                    class_obj = box_list[class_id]
                    save_file.write(':')
                    for obj in class_obj:
                        for elem in obj:
                            save_file.write(elem + ' ')
                save_file.write('\n')

if __name__ == '__main__':

    list_path = "data/kitti/imglists/val_image.list"
    src_path  = "/rawdata/liulingbo/3d_detection/kitti/train_val_dataset/left_eye/training_label/training/label_2/"
    save_path = "data/kitti/imglists/val.lst"
    
    generate(list_path, src_path, save_path)
