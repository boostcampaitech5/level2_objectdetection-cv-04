import json
import os
import random
from sklearn.model_selection import StratifiedGroupKFold
import numpy as np
import pandas as pd

def split_dataset(input_json, output_dir):
    #random.seed(random_seed)

    with open(input_json) as json_reader:
        dataset = json.load(json_reader)

    images = dataset['images']
    # images = dataset['image_id'] # -> 이렇게 되어야 하는게 아
    annotations = dataset['annotations']
    categories = dataset['categories']
    
    # file_name에 prefix 디렉토리까지 포함 (CocoDataset 클래스를 사용하는 경우)
    # for image in images:
    #     image['file_name'] = '{}/{}'.format(image['file_name'][0], image['file_name'])

    image_ids = [x.get('id') for x in images]
    image_ids.sort()
    # TODO 비율에 맞게 validation json 파일 만들기

    random.shuffle(image_ids)
    
    var = [(ann["image_id"], ann["category_id"]) for ann in annotations]
    X = np.ones((len(annotations), 1))
    y = np.array([v[1] for v in var])
    groups = np.array([v[0] for v in var])

    cv = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=411)
    fold4_train = []
    fold4_val = []
    for idx, (train_idx, val_idx) in enumerate(cv.split(X, y, groups)):
        if idx == 4:
            fold4_train = groups[train_idx]
            fold4_val = groups[val_idx]
            # print("TRAIN:", fold4_train)
            # print(" ", y[train_idx])
            # print(" TEST:", fold4_val)
            # print(" ", y[val_idx])


    # num_val = int(len(image_ids) * val_ratio)
    # num_train = len(image_ids) - num_val
    image_ids_train = []
    for idx in list(set(fold4_train)):
        image_ids_train.append(image_ids[idx])
        
    image_ids_val = []
    for idx in list(set(fold4_val)):
        image_ids_val.append(image_ids[idx])
 
    # #이것을 train_idx, val_idx로 
    # image_ids_val, image_ids_train = set(image_ids[:num_val]), set(image_ids[num_val:])

    #각 index에 해당하는 데이터 뽑음 
    train_images = [x for x in images if x.get('id') in image_ids_train]
    val_images = [x for x in images if x.get('id') in image_ids_val]
    train_annotations = [x for x in annotations if x.get('image_id') in image_ids_train]
    val_annotations = [x for x in annotations if x.get('image_id') in image_ids_val]

    #json파일 만들기 
    train_data = {
        'images': train_images,
        'annotations': train_annotations,
        'categories': categories,
    }

    val_data = {
        'images': val_images,
        'annotations': val_annotations,
        'categories': categories,
    }

    # output_seed_dir = os.path.join(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    output_train_json = os.path.join(output_dir, 'train.json')
    output_val_json = os.path.join(output_dir, 'val.json')
    # output_train_csv = os.path.join(output_dir, 'train.csv')
    # output_val_csv = os.path.join(output_dir, 'val.csv')

    print(f'write {output_train_json}')
    with open(output_train_json, 'w') as train_writer:
        json.dump(train_data, train_writer)

    print(f'write {output_val_json}')
    with open(output_val_json, 'w') as val_writer:
        json.dump(val_data, val_writer)

    # print(f'write {output_train_csv}, {output_val_csv}')
    # with open(input_csv, 'r') as csv_reader, \
    #         open(output_train_csv, 'w') as train_writer, \
    #         open(output_val_csv, 'w') as val_writer:
    #     train_writer.write('ImageId,EncodedPixels,Height,Width,CategoryId\n')
    #     val_writer.write('ImageId,EncodedPixels,Height,Width,CategoryId\n')
    #     for line in csv_reader:
    #         if line.startswith('ImageId'): continue
    #         image_id, encoded_pixels, height, width, category_id = line.strip().split(',')
    #         image_id = int(image_id)
    #         if image_id in image_ids_train:
    #             train_writer.write(line)
    #         elif image_id in image_ids_val:
    #             val_writer.write(line)
    #         else:
    #             raise ValueError(f'unknown image_id: {image_id}')

input_json = '/opt/ml/dataset/train.json'
output_dir = '/opt/ml/dataset/split_dataset/'
split_dataset(input_json, output_dir)
