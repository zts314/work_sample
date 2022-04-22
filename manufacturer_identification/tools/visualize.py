import argparse
import os
from itertools import chain
import cv2
import tqdm

from detectron2.data import DatasetCatalog, MetadataCatalog
from detectron2.data import detection_utils as utils
from detectron2.data.datasets.coco import register_coco_instances
from detectron2.utils.logger import setup_logger
from detectron2.utils.visualizer import Visualizer

def parse_args(in_args=None):
    parser = argparse.ArgumentParser(description="Visualize ground-truth data")

    parser.add_argument("--image_root", metavar="FILE", help="path to config file")
    parser.add_argument("--annotations_json", metavar="FILE", help="path to config file")
    return parser.parse_args(in_args)


if __name__ == "__main__":
    args = parse_args()
    logger = setup_logger()
    logger.info("Arguments: " + str(args))

    register_coco_instances('this_split', {}, json_file=args.annotations_json, image_root=args.image_root)
    metadata = MetadataCatalog.get('this_split')


    def output(vis, fname):
        print(fname)
        cv2.imshow("window", vis.get_image()[:, :, ::-1])
        cv2.waitKey()

    dicts = list(chain.from_iterable([DatasetCatalog.get('this_split')]))

    for dic in tqdm.tqdm(dicts):
        img = utils.read_image(dic["file_name"], "RGB")
        visualizer = Visualizer(img, metadata=metadata, scale=1.0)
        vis = visualizer.draw_dataset_dict(dic)
        output(vis, os.path.basename(dic["file_name"]))
