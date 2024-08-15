from os import walk
from os import path
from os import makedirs
from os import scandir
import argparse

from pydub import AudioSegment
from pydub.silence import split_on_silence

OUTPUT_DIR = 'split_on_silence'
MAX_DURATION = 10000

MORE_THAN_TEN_DIR = 'more_than_10_seconds'
LESS_THAN_TEN_DIR = 'less_than_10_seconds'

global_counter = 0

def create_filename(duration: int, output_dir: str):
    global global_counter

    prefix = f'LOU{str(global_counter).zfill(7)}'
    filename = f'{prefix}_{duration}ms.wav'
    global_counter += 1

    return path.join(output_dir, filename)

def process_file(output_dir: str, args: argparse.Namespace, split_dirs: dict):
    audio = AudioSegment.from_file(output_dir, format='wav')

    chunks = split_on_silence(
            audio,
            min_silence_len=args.min_silence,
            silence_thresh=args.silence_thresh,
            keep_silence=args.keep_silence,
            )

    for _, chunk in enumerate(chunks):
        dur= len(chunk)
        output_dir = split_dirs['more_than_ten' if dur > MAX_DURATION else 'less_than_ten']
        filename = create_filename(dur, output_dir)
        chunk.export(filename, format='wav')
        print(f'Exported chunk with duration {dur:>7}ms.')
        

arg_parser = argparse.ArgumentParser(
    prog='split_on_silence',
    description=f"""
    This program processes a directory of audio files by splitting them at points of silence. 
    After splitting, the resulting audio segments are categorized based on their duration:
    
    - Segments longer than 10 seconds are saved to a specified directory for longer files.
    - Segments shorter than 10 seconds are saved to a specified directory for shorter files.

    The current script max duration is set to {MAX_DURATION/100} seconds.
    """
)

arg_parser.add_argument('dataset_dir', help='Input directory')
arg_parser.add_argument('--min-silence', type=int, default=500, help='Minimum silence length in milliseconds')
arg_parser.add_argument('--silence-thresh', type=int, default=-40, help='Silence threshold in dBfs')
arg_parser.add_argument('--keep-silence', type=int, default=50, help='The amount of silence to keep at the beginning and end of the audio segment')
args = arg_parser.parse_args()

output_dir = path.join(args.dataset_dir, '..', OUTPUT_DIR)
split_dirs = {'more_than_ten': path.join(output_dir, MORE_THAN_TEN_DIR), 'less_than_ten': path.join(output_dir, LESS_THAN_TEN_DIR)}

if not path.exists(output_dir):
    print('Creating output directory: ', output_dir)

elif any(scandir(output_dir)):
    print(f'Output directory "{output_dir}" is not empty. Exiting...')
    exit(1)

makedirs(output_dir, exist_ok=True)

print(f'creating split subdirectories "{split_dirs['more_than_ten']}" and "{split_dirs['less_than_ten']}"...')

makedirs(split_dirs['more_than_ten'], exist_ok=True)
makedirs(split_dirs['less_than_ten'], exist_ok=True)

print(f'Iterating over files in the dataset directory "{args.dataset_dir}"...')

for root, dirnames, filenames in walk(args.dataset_dir):
    for filename in filenames:
        if filename.endswith('.wav'):
            try:
               process_file(path.join(root, filename), args, split_dirs)
            except Exception as e:
                print(f'Error processing file: {filename}. Error: {e}.\n\nSkipping....')
        else:
            print('Only .wav files allowed. Skipping file: ', filename)
    



