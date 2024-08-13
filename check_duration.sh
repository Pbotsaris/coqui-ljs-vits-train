#!/bin/bash

if [ -z "S1" ]; then
   printf "Usage: check_duration.sh <path to dataset wavs>\n"
   exit 1
fi
report=""

for file in $1/*.wav; do
   dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$file")
   dur_round=${dur%.*}

   if [ "$dur_round" -lt 1 ]; then
      report+="File $file is less than 1 seconds long: $dur seconds\n"
      printf "F"
   else
      printf "."
   fi
done

echo "\n Report:"
echo "$report"


