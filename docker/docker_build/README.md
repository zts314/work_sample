# Zack Steck - Work Sample

This repository contains code for 3 work samples. 2 of the work samples are listed as "complete", with emphasis on 
the parenthesis. As there are many more possibilities to explore (Focal loss, WEFT classifiers, self-supervised learning, etc.), 
I don't consider them to be truly complete. However, Please consider my submissions in the following order 
(in both time and GPU cycles spent):

1. Manufacturer Identification - "Complete"
2. Geological Similarity - "Complete"

___
# Installation

## Anaconda

The `environment.yml` in the root of this directory can be used to create an anaconda environment. To setup this 
repository using anaconda, run the following command from the root of the repository:

```
conda env create -f environment.yml
```

## Docker

### 1. Build the container
The `docker` folder in the root of this repository contains a bash script that will build a docker container with all necessary dependencies required 
to run this repository. To build the docker container, from the root of this repository, run:

```
cd docker
./build_docker.sh
```

The build will take some time as Detectron2 requires Pycocotools, which leans on gcc (so I couldn't use a pre-built pytorch container, sadly).

### 2. Run the container

The above commands will create a docker image called `zsteck:1.0.0`. To run the container, run the `run_interactive.sh` 
bash script or run the following command:

```
docker run -it --ipc=host
```

______

## Manufacturer Identification ("Complete") - At a Glance

### How to run

1. 

### Experiments Run

#### Baseline Experiment
* Data: Converted to COCO
* Model: Resnet50 Faster-RCNN FPN, COCO Pretrained weights

|   AP   |  AP50  |  AP75  |  APs  |  APm  |  APl   |
|:------:|:------:|:------:|:-----:|:-----:|:------:|
| 91.412 | 96.600 | 95.829 |  nan  |  nan  | 91.412 |

| category                 | AP     | category             | AP     | category             | AP     |
|:-------------------------|:-------|:---------------------|:-------|:---------------------|:-------|
| ATR                      | 96.341 | Airbus               | 93.161 | Antonov              | 94.794 |
| Beechcraft               | 92.867 | Boeing               | 94.067 | Bombardier Aerospace | 92.853 |
| British Aerospace        | 90.460 | Canadair             | 93.872 | Cessna               | 89.677 |
| Cirrus Aircraft          | 89.984 | Dassault Aviation    | 95.668 | Dornier              | 91.257 |
| Douglas Aircraft Company | 82.414 | Embraer              | 95.371 | Eurofighter          | 93.373 |
| Fairchild                | 92.097 | Fokker               | 93.718 | Gulfstream Aerospace | 91.910 |
| Ilyushin                 | 91.306 | Lockheed Corporation | 84.836 | Lockheed Martin      | 94.088 |
| McDonnell Douglas        | 87.587 | Panavia              | 94.274 | Piper                | 86.103 |
| Robin                    | 90.450 | Saab                 | 96.454 | Supermarine          | 77.434 |
| Tupolev                  | 94.180 | Yakovlev             | 92.042 | de Havilland         | 89.724 |

#### Class Balanced Experiment
* Data: Converted to COCO, Custom WeightedRandomSampler
* Model: Resnet50 Faster-RCNN FPN, COCO Pretrained weights

# TODO: Paste in class-balanced results

### Future Directions

Some obvious directions include obtaining more data to train on from publicly available datasets. Other more exotic 
things to try include:
1. Leveraging a smarter loss function. Something like Reduced Focal Loss, which won the xView competition back in 2018
   (a notoriously long-tailed dataset), could help to overcome the class imbalance even better. That being said, this 
   would be more complex to implement as it would require modifying the Faster-RCNN FPN and Class head loss functions.
2. Performing downstream classifier fusion. It would be interesting to take the detected bounding boxes/labels and 
   construct a fusion approach (using logistic regression or something simple) that would ingest the output of WEFT 
   classifiers to help boost performance. The WEFT (Wings Engine Fuselage and Tail) classifiers would be downstream recognition
models that would attempt to ingest the detected object chip and classify sum attributes about the aircraft (e.g. number of engines, 
wingspan, engine type, etc.).

## Geological Similarity ("Complete") - At a Glance

### How to run

1. Run the 

### Future Directions
