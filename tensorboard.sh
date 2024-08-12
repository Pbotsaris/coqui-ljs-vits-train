#!/bin/bash


# this script will tunnel the tensorboard port to your local machine
# via ssh. This is useful when you are running tensorboard on a remote

if [ -z "$1" ]; then
   printf "Usage: tensorboard.sh <the ip of the instance>\n"
   exit 1
fi
ssh -N -f -L localhost:6006:localhost:6006 ubuntu@"$1"


