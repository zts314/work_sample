#!/bin/bash

CONTEXT="./docker_build"
IMG="zsteck"
TAG="1.0.0"

while [[ $# -gt 0 ]]; do
  case $1 in
    -i|--image)
      IMG="$2"
      shift # past argument
      shift # past value
      ;;
    -t|--tag)
      TAG="$2"
      shift # past argument
      shift # past value
      ;;
    -*|--*)
      echo "Unknown option $1"
      exit 1
      ;;
  esac
done

if [ ! -d $CONTEXT ]
then
    mkdir $CONTEXT
fi

rsync -av --exclude='notebooks/output' --exclude='notebooks/output_class_balanced' ../manufacturer_identification $CONTEXT/manufacturer_identification
rsync -av --exclude='../geological_similarity/output' ../geological_similarity $CONTEXT/geological_similarity

cp Dockerfile $CONTEXT

docker build -t $IMG:$TAG ./$CONTEXT