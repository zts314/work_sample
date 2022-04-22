# Installation

## Anaconda

The `environment.yml` in the root of this directory can be used to create an anaconda environment. To setup this 
repository using anaconda, run the following command from the root of the repository:

```
conda env create -f environment.yml
```

## Docker

Was built using Docker version 20.10.14, build a224086

### 1. Build the container or pull from docker hub
The `docker` folder in the root of this repository contains a bash script that will build a docker container with all necessary dependencies required 
to run this repository. To build the docker container, from the root of this repository, run:

**Install Nvidia container toolkit for container GPU access**:

If you don't plan to run the notebooks but just view them, feel free to skip this step. These instructions are for Ubuntu 20.04, but instructions for
other distros can be found [here](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#linux-distributions).
To ensure we have access to the GPUs inside the container, please run the following command:

Setup the repository and GPG key:

```
distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
      && curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
      && curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
            sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
            sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
```

Install Nvidia container toolkit:

```
 sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
```

**Build the container**:
```
cd docker
./build_docker.sh
```

The build will take some time as Detectron2 requires Pycocotools, which leans on gcc (so I couldn't use a pre-built pytorch container, sadly).

Alternatively, if you don't wish to build the container from scratch, the container can be pulled from docker hub using the following command:

```
docker pull zts314/work_sample:1.0.1
```

### 2. Run the container

The above commands will create a docker image called `zsteck:1.0.0`. To run the container, run the `run_container.sh` bash script. 
If you wish to run the notebooks on your data, then please run the following command, taking care to mount your data directory:

**Without GPU capabilities**:

Run this command if you don't have `nvidia-container-toolkit` installed.

```
docker run --rm -it --ipc=host -p 9000:9000 -v /path/to/data/on/host:/home/appuser/data zsteck:1.0.0
```

**With GPU capabilities**:

Run this command if you have `nvidia-container-toolkit` installed.

```
docker run --rm -it --gpu all --ipc=host -p 9000:9000 -v /path/to/data/on/host:/home/appuser/data zsteck:1.0.0
```