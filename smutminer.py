#!/usr/bin/env python3

import signal
import argparse
import string
import os
import sys
import numpy
import shutil
from PIL import Image
from io import BytesIO

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' # Suppress Tensorflow log messages
import opennsfw2

NSFW_MODEL_DIR = os.path.dirname(os.path.abspath(__file__))

parser = argparse.ArgumentParser()
parser.add_argument('command', nargs=1, type=str, choices=['move', 'copy', 'link', 'score'], default='score', help='Action to take, default: Print the image path and NSFW Score to stdout')
parser.add_argument('-t', '--threshold', type=float, default=.7, help='Default matching threshold for the open_nsfw model (0 - 1). Default: .7')
parser.add_argument('-l', '--list', action=argparse.BooleanOptionalAction,  help='Print a list of original file paths')
parser.add_argument('directory', nargs='?', type=str, default='./', help='Input Directory. Default: current working directory.')
parser.add_argument('output', nargs='?', type=str, default='nsfw', help='Output Subdirectory. Default: nsfw')
args = parser.parse_args()

COMMAND = args.command[0]
SCORE_THRESHOLD = args.threshold
INPUT_DIR = os.path.abspath(args.directory)
OUTPUT_DIR = os.path.abspath(os.path.join(INPUT_DIR, args.output))
EXCLUDE = set([args.output])

def handler(signum, frame):
    print("\nSignal Caught, exiting.")
    os._exit(1)

def preprocess_and_compute(pimg, model):
    image = opennsfw2.preprocess_image(Image.open(BytesIO(pimg)), opennsfw2.Preprocessing.YAHOO)
    inputs = numpy.expand_dims(image, axis=0)
    return model.predict(inputs, verbose=0)

def main():

    if COMMAND != "score":
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)

    if args.list:
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
        filelist = open(os.path.join(OUTPUT_DIR, 'originalpaths.txt'), 'w')

    # Pre-load Tensorflow OpenNSFW2 model
    #print("Loading OpenNSFW2 model")
    model = opennsfw2.make_open_nsfw_model()

    #print("Recursively scanning directory " + INPUT_DIR)
    for fulldir, subdir, files in os.walk(INPUT_DIR):
        subdir[:] = [d for d in subdir if d not in EXCLUDE] # Exclude the output directory
        for filename in files:
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.tif', '.bmp', '.gif')):
                try:
                    sys.stderr.write("\033[K")
                    print(os.path.join(fulldir, filename), "scoring...", end='\r', file=sys.stderr)
                    sys.stderr.flush()

                    image_data = open(os.path.join(fulldir, filename), 'rb').read()
                    scores = preprocess_and_compute(image_data, model)
                except:
                    continue

                if scores[0][1] >= SCORE_THRESHOLD:
                    if args.list:
                        filelist.write(os.path.join(fulldir, filename) + "\n")
                        filelist.flush()
                    if COMMAND == "move":
                        shutil.move(os.path.join(fulldir, filename), os.path.join(OUTPUT_DIR, filename))
                    elif COMMAND == "copy":
                        shutil.copy(os.path.join(fulldir, filename), os.path.join(OUTPUT_DIR, filename))
                    elif COMMAND == "link":
                        os.symlink(os.path.join(fulldir, filename), os.path.join(OUTPUT_DIR, filename))

                    sys.stdout.write("\033[K")
                    print(os.path.join(fulldir, filename), "NSFW score:" , scores[0][1])
                        
            
            else:
                sys.stderr.write("\033[K")
                print(os.path.join(fulldir, filename), "is not a supported image.", end='\r', file=sys.stderr)
                sys.stderr.flush()

    if args.list:
        filelist.close()

signal.signal(signal.SIGINT, handler)

if __name__ == '__main__':
    main()