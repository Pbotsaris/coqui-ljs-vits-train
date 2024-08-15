# TTS to explore

- silero: [https://github.com/snakers4/silero-models](https://github.com/snakers4/silero-models)
- piper: [https://github.com/rhasspy/piper?tab=readme-ov-file](https://github.com/rhasspy/piper?tab=readme-ov-file)



### VIts training

- bach 1: Default

#### batch 2:
- decreased learning rates to 0.0001
- increased batch size to 64
- increased eval batch size to 32
- increased batch group size to 6
- increased feature loss alpha by 0.1


# Notes on metrics

- TrainEpochStats/avg_loss_1 is the an indicator that the model is overfitting when it shows a divergence and the value increases here. [more](https://github.com/coqui-ai/TTS/discussions/1053).
- TrainEpochStats/avg_loss_1 is the best metric to see loss.



##  Random notes

Investigate this
> I've got YourTTS working amazingly! Some of the samples were almost perfect. I developed a ton of tricks - replacements to the whisper text, not using demux (just diarizing everything and using VAD to cut out samples with audio) and a few other techniques. If you'd like to collaborate I can send an email or something. Saw you left the YourTTS track but maybe worth another look.

> If you haven't tried deepfilternet for denoise, try poking around its command line application. Easy to use and works really well a lot of the time. Voicefixer is another, but it's a bit of a pain.


### Explore in the future

https://github.com/JarodMica/ai-voice-cloning

https://github.com/jasonppy/VoiceCraft?tab=readme-ov-file#environment-setup


GPT-SoVITS
Play HT 2.0

OpenVoice V2
XTTSv2


## Cleaning Lou's Dataset Log
First we need to split the audio files so that they have no more than 10 seconds

1. used the script `script/strip_silence.py` to strip silence from all the files using defaults
2. then ran the `script/split_on_silence.py` again with the following settings

         python split_on_silence.py --min-silence 110 --silence-thresh -60 --keep-silence 30 ~/storage/datasets/louspeech/test/
3. The script writes the duration of the file in in milliseconds in the filename. Next step is to remove anything smaller than 1 second.


## next exploration

- maybe too strong discrimitator
