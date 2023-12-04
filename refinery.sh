#!/usr/bin/env bash

# A wrapper around smutminer.py and photorec to recover NSFW images
# from raw drives or drive images. Update the shell variables below
# then run this script with a device name.

IMAGE_DIR="$HOME/storage/images"
REC_DIR="$HOME/scratch/recovery"
OUTPUT_DIR="$HOME/scratch/nsfw"

if [ $# -ne 1 ]
then
    echo "Usage: $0 <device>"
    exit 1
fi

DEVICE=$1

if [ ! -b $DEVICE ]
then
    echo "$DEVICE is not a block device or does not exist"
    exit 1
fi

if ! command -v photorec &> /dev/null
then
    echo "Photorec is not in the default path. Please install TestDisk."
    exit 1
fi

if ! command -v ddrescue &> /dev/null
then
    echo "ddrescue is not in the default path. Please install GNU ddrescue."
    exit 1
fi

clear

SERIAL=$(udevadm info --query=all --name=$DEVICE | grep ID_SERIAL_SHORT | cut -d "=" -f 2)
OUTPUT_DIR="$OUTPUT_DIR/$SERIAL"
REC_DIR="$REC_DIR/$SERIAL"

mkdir -p "$IMAGE_DIR" || exit 1
mkdir -p "$REC_DIR/recovered" || exit 1
mkdir -p "$OUTPUT_DIR" || exit 1

clear
echo "The following functions require root access."
#sudo dd if=$DEVICE of=$IMAGE_DIR/$SERIAL.img bs=1M
sudo ddrescue $DEVICE $IMAGE_DIR/$SERIAL.img $IMAGE_DIR/$SERIAL.map || exit 1
clear
photorec /d "$REC_DIR/recovered" /cmd "$IMAGE_DIR/$SERIAL.img" partition_none,wholespace,fileopt,everything,disable,jpg,enable,png,enable,tif,enable,gif,enable,bmp,enable,search || exit 1
clear
./smutminer.py -l copy "$REC_DIR" "$OUTPUT_DIR" || exit 1
