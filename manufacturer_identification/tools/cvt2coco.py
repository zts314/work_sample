import os
import argparse
import json
import pandas as pd
from typing import List, Dict
from tqdm import tqdm
import rasterio


def get_image_info(img_root: str, images_in_split: List = []):
    image_info = []
    image_name_to_id_map = {}
    image_to_width_height_map = {}
    to_process = [(os.path.join(img_root, x), x) for x in os.listdir(img_root)]
    # To ensure sequential ids, track with iterator instead of enumerate
    id = 0
    for file_path, file_name in tqdm(to_process, desc='Constructing image list...'):
        if len(images_in_split) > 0 and file_name not in images_in_split: continue
        raster = rasterio.open(file_path)
        image_info.append({
            'file_name': file_name,
            'height': raster.height,
            'width': raster.width,
            'id': id
        })
        image_name_to_id_map[file_name] = id
        image_to_width_height_map[file_name] = (raster.height, raster.width)
        id += 1
    return image_info, image_name_to_id_map, image_to_width_height_map


def get_annotation_info(box_coords_file: str,
                        split_box_labels: Dict,
                        label_to_id_map: Dict,
                        image_name_to_id_map: Dict,
                        image_dimensions: Dict,
                        images_in_split: List = []):
    image_info = []
    # Load in the box coords file, ensuring the dtypes are correct
    box_coords = pd.read_csv(box_coords_file, delimiter=' ', header=None, dtype={0: str, 1: int, 2: int, 3: int, 4: int})
    box_coords.columns = ['image_name', 'min_x', 'min_y', 'max_x', 'max_y']
    id = 0
    for i, row in box_coords.iterrows():
        image_name = str(row.image_name) + '.jpg'
        if len(images_in_split) > 0 and image_name not in images_in_split: continue
        image_id = image_name_to_id_map[image_name]
        category_id = label_to_id_map[split_box_labels[image_name]]
        height, width = image_dimensions[image_name]
        min_x, min_y, max_x, max_y = row[1:]
        min_x = max(0, min_x)
        min_y = max(0, min_y)
        max_x = min(max_x, width)
        max_y = min(max_y, height)
        w = max_x - min_x
        h = max_y - min_y
        image_info.append({
            'id': id,
            'image_id': image_id,
            'bbox': [min_x, min_y, w, h],
            'area': w * h,
            'iscrowd': 0,
            'category_id': category_id
        })
        id += 1
    return image_info


def convert_to_cocojson(box_coords_file,
                        box_labels_file,
                        image_root,
                        labels_file,
                        output_path):
    # Load the labels file
    with open(labels_file, 'r') as f:
        labels = [x.rstrip('\n') for x in f.readlines()]

    label_to_id_map = {x: i for i, x in enumerate(labels)}

    # Load the labels for each box/image
    split_box_labels = {}
    with open(box_labels_file, 'r') as f:
        # Read in the lines from the box_labels file, removing bad chars
        lines = [x.rstrip('\n') for x in f.readlines()]
        # Split off the image_id
        for line in lines:
            split_line = line.split(' ')
            split_box_labels[split_line[0] + '.jpg'] = ' '.join(split_line[1:])

    image_info, image_name_to_id_map, image_to_width_height_map = get_image_info(image_root, images_in_split=split_box_labels.keys())

    output_json_dict = {
        "images": image_info,
        "annotations": get_annotation_info(box_coords_file,
                                           label_to_id_map=label_to_id_map,
                                           split_box_labels=split_box_labels,
                                           image_name_to_id_map=image_name_to_id_map,
                                           image_dimensions=image_to_width_height_map,
                                           images_in_split=split_box_labels.keys()),
        "categories": [{'name': x, 'id': i} for i, x in enumerate(labels)]
    }

    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
    print(f'Writing results to {os.path.basename(output_path)} with {len(output_json_dict["images"])} images and {len(output_json_dict["annotations"])} annotations')
    with open(output_path, 'w') as f:
        output_json = json.dumps(output_json_dict, indent=4)
        f.write(output_json)


def main():
    parser = argparse.ArgumentParser(
        description='This script support converting voc format xmls to coco format json')
    parser.add_argument('--box_coords', type=str, default=None,
                        help='Path to txt file containing img_name, box_coords in (min_x, min_y, max_x, max_y)')
    parser.add_argument('--box_labels', type=str, default=None,
                        help='Path to split entry containing image_name, target_label tuples')
    parser.add_argument('--image_root', type=str, default=None,
                        help='Path to image root directory.')
    parser.add_argument('--labels', type=str, default=None,
                        help='Path to label list')
    parser.add_argument('--output', type=str, default='output.json', help='path to output json file')

    args = parser.parse_args()

    convert_to_cocojson(
        box_coords_file=args.box_coords,
        box_labels_file=args.box_labels,
        image_root=args.image_root,
        labels_file=args.labels,
        output_path=args.output
    )


if __name__ == '__main__':
    main()
