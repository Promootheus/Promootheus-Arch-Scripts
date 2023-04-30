#!/bin/bash

# Install miniconda

wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod +x Miniconda3-latest-Linux-x86_64.sh
./Miniconda3-latest-Linux-x86_64.sh

# type yes

# yes to conda init

conda --version

git clone https://github.com/neonbjb/tortoise-tts.git
cd tortoise-tts

# python -m pip install -r ./requirements.txt
# python setup.py install

# Step 2: Create Conda environment
conda create -n tortoise python=3.10
conda activate tortoise

# Step 3: Install PyTorch - use conda command https://pytorch.org/get-started/locally/

# e.g conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia

# within /home/promootheus/Documents/tortoise-tts/

touch tts.py

paste in


# tts.py
import torch
import torchaudio
import torch.nn as nn
import torch.nn.functional as F
from tortoise.api import TextToSpeech
from tortoise.utils.audio import load_audio, load_voice, load_voices

# This will download all the models used by Tortoise from the HuggingFace hub.
tts = TextToSpeech()

# This is the text that will be spoken.
text = "Thanks for reading this article. I hope you learned something."

# Pick a "preset mode" to determine quality. Options: {"ultra_fast", "fast" (default), "standard", "high_quality"}. See docs in api.py
preset = "fast"

CUSTOM_VOICE_NAME = "tom"

voice_samples, conditioning_latents = load_voice(CUSTOM_VOICE_NAME)

gen = tts.tts_with_preset(text, voice_samples=voice_samples, conditioning_latents=conditioning_latents, preset=preset)

torchaudio.save(f'generated-{CUSTOM_VOICE_NAME}.wav', gen.squeeze(0).cpu(), 24000)


# SAVE

python tts.py


# Need to get the compatible version of pydantic

pip uninstall pydantic
pip install pydantic==1.9.1

#This script allows you to speak a single phrase with one or more voices.
#python tortoise/do_tts.py --text "I'm going to speak this" --voice random --preset fast

#This script provides tools for reading large amounts of text.

#python tortoise/read.py --textfile <your text to be read> --voice random
