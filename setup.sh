#!/bin/bash

if [ -z "$1" ]; then
   printf "Usage: setup.sh <path to download dataset>\n"
   exit 1
fi

if [ -d 'venv' ]; then
   printf "venv directory already exists. activating envirioment\n"
   source venv/bin/activate
 else
   printf "Creating virtual environment\n"
   python -m venv venv
   source venv/bin/activate
fi

dataset_path=$1

if [ -d 'vendor' ]; then
    printf "vendor directory already exists. Skipping cloning coqui-TTS\n"
 else
printf "Cloning coqui-TTS to vendor\n"
git clone https://github.com/Pbotsaris/coqui-TTS.git vendor

fi

cd vendor

# will make a venv here so the deps coqui deps don't conflict with whatever is pre-installed in gpu farm system
pip install -e .
cd ..

printf "Downloading dataset to $dataset_path\n"

if [ -d "$dataset_path" ]; then
    printf "Dataset directory already exists. Skipping...\n"
 else
mkdir -p $dataset_path
wget -O $dataset_path/LJSpeech-1.1.tar.bz2 https://data.keithito.com/data/speech/LJSpeech-1.1.tar.bz2 
printf "Extracting dataset..\n"
tar -xvf $dataset_path/LJSpeech-1.1.tar.bz2 -C $dataset_path
printf "Dataset downloaded and extracted to $dataset_path\n"
fi

printf "Setting DATASET_PATH envirioment variable\n"
export DATASET_PATH="$dataset_path"/LJSpeech-1.1

