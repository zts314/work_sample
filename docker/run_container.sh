#!/bin/bash

docker run --rm -it --ipc=host -p 9000:9000 -v /path/to/data/on/host:/home/appuser/data zsteck:1.0.0

echo "Don't forget to change the data path above to your data root."