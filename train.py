# import torch
import os
import sys

# Models & Configs
from vendor.TTS.tts.configs.shared_configs import BaseDatasetConfig
from vendor.TTS.tts.configs.vits_config import VitsConfig
from vendor.TTS.tts.models.vits import Vits, VitsAudioConfig

# Processors
from vendor.TTS.utils.audio import AudioProcessor
from vendor.TTS.tts.utils.text.tokenizer import TTSTokenizer

# Training
import vendor.TTS.tts.datasets as datasets

# trainer is in a separated project on https://github.com/eginhard/coqui-trainer
# this is installed in vendor with cd vendor; pip install -e .
from trainer import Trainer, TrainerArgs 

OUTPUT="output"

if not os.path.exists(OUTPUT):
    print(f"Creating output directory: {OUTPUT}")

os.makedirs(OUTPUT, exist_ok=True)
outpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), OUTPUT)

print(f'Checkpoints will be saved in {outpath}')

dataset_path = os.getenv("DATASET_PATH")

if  dataset_path is None:
    print("Please set the DATASET_PATH environment variable.")
    sys.exit(1)

print("Setting up dataset: Using dataset path:", dataset_path)
dataset_config = BaseDatasetConfig(
        formatter="ljspeech", meta_file_train="metadata.csv", path=dataset_path
        )

audio_config = VitsAudioConfig(
        sample_rate=22050, win_length=1024, hop_length=256, num_mels=80, mel_fmin=0, mel_fmax=None
        )

print("Setting up Vits Config")
vits_config = VitsConfig(
    audio=audio_config,
    lr_gen=0.0002,
    lr_disc=0.0002,
    run_name="vits_ljspeech",
    batch_size=86,
    eval_batch_size=16,
    batch_group_size=5,
    num_loader_workers=8,
    num_eval_loader_workers=4,
    run_eval=True,
    test_delay_epochs=-1,
    epochs=1000,
    text_cleaner="english_cleaners",
    use_phonemes=True,
    phoneme_language="en-us",
    phoneme_cache_path=os.path.join(outpath, "phoneme_cache"),
    compute_input_seq_cache=True,
    print_step=25,
    print_eval=True,
    mixed_precision=False,
    feat_loss_alpha=1.0,
    output_path=outpath,
    datasets=[dataset_config],
    cudnn_benchmark=False,
    )

print("Setting up tokenizer and audio processor.")
audio_processor = AudioProcessor.init_from_config(vits_config)
tokenizer, vits_config = TTSTokenizer.init_from_config(vits_config)

train_samples, eval_samples = datasets.load_tts_samples(
        dataset_config,
        eval_split=True,
        eval_split_max_size=vits_config.eval_split_max_size,
        eval_split_size=vits_config.eval_split_size,
)

print("Setting up model.")
model = Vits(vits_config, audio_processor, tokenizer, speaker_manager=None)


print("start training....")
train = Trainer(
        TrainerArgs(),
        vits_config,
        model=model,
        train_samples=train_samples,
        eval_samples=eval_samples,
        output_path=outpath,
        )

train.fit();
