# smutminer

Extract/Score images from local directory structures. Updated for Tensorflow2 and OpenNSFW2

### [Install and configure Tensorflow](https://www.tensorflow.org/install/pip#ubuntu_1804_cuda_101)

### Install Miniconda
- `curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -o Miniconda3-latest-Linux-x86_64.sh`
- `bash Miniconda3-latest-Linux-x86_64.sh`

### Create a conda environment

- `conda create --name opennsfw2 python=3.9`
- `conda activate opennsfw2`

### GPU Setup

- `conda install -c conda-forge cudatoolkit=11.2 cudnn=8.1.0`
- `export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CONDA_PREFIX/lib/`
- `mkdir -p $CONDA_PREFIX/etc/conda/activate.d`
- `echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CONDA_PREFIX/lib/' > $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh`

### Install TensorFlow

- `pip install --upgrade pip`
- `pip install tensorflow`

## Install other requirements

Ensure the correct conda environment is activated and run

- `pip install -r requirements.txt`

## Running

Activate the conda environment you created above

- `conda activate opennsfw2`

```
smutminer.py -h
usage: smutminer.py [-h] [-t THRESHOLD] [-l | --list | --no-list] {move,copy,link,score} [directory] [output]

positional arguments:
  {move,copy,link,score}
                        Action to take, default: Print the image path and NSFW Score to stdout
  directory             Input Directory. Default: current working directory.
  output                Output Subdirectory. Default: nsfw

options:
  -h, --help            show this help message and exit
  -t THRESHOLD, --threshold THRESHOLD
                        Default matching threshold for the open_nsfw model (0 - 1). Default: .7
  -l, --list, --no-list
                        Print a list of original file paths
```
