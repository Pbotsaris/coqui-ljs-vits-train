#!/bin/bash

output_dir=$3

if [ -z "$output_dir" ]; then
  output_dir="output.wav"
fi


tts --text "$2" \
      --model_path "$1" \
      --config_path $(dirname "$1")/"config.json" \
      --out_path $output_dir
