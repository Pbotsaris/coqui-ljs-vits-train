if [ -z "$1" ]; then
   printf "Usage: setup.sh <path to download dataset>\n"
   exit 1
fi

dataset_path=$1

if [ -d 'vendor' ]; then
    printf "vendor directory already exists. Skipping cloning coqui-TTS\n"
 else
printf "Cloning coqui-TTS to vendor\n"
git clone git@github.com:Pbotsaris/coqui-TTS.git vendor
fi

cd vendor
pip install -e .
cd ..

printf "Downloading dataset to $dataset_path\n"

if [ -d "$dataset_path" ]; then
    printf "Dataset directory already exists. Cleaning up...\n"
    rm -rf $dataset_path
    mkdir -p $dataset_path
fi

mkdir -p $dataset_path
wget -O $dataset_path/LJSpeech-1.1.tar.bz2 https://data.keithito.com/data/speech/LJSpeech-1.1.tar.bz2 
tar -xf $dataset_path/LJSpeech-1.1.tar.bz2 -C $dataset_path

printf "Dataset downloaded and extracted to $dataset_path\n"

printf "Setting DATASET_PATH envirioment variable\n"
export DATASET_PATH="$dataset_path"/LJSpeech-1.1

