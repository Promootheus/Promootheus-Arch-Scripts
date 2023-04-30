 
# Install Tortoise-TTS-Fast

# It is always recommended to use a clean and new environment for each project. 
# Install Anaconda for dealing with different Python environments:

wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
source ~/.bashrc

# Once Anaconda is installed, we can create a virtual environment for this project:

conda create -n tts-fast python=3.8
conda activate tts-fast

# Clone the tortoise-tts-fast library. 
# Here we will use thisserand fork to be able to upload and create new 
# voices within the web UI.

git clone https://github.com/thisserand/tortoise-tts-fast.git
cd tortoise-tts-fast

# Install all required libraries to run the Tortoise-TTS model:

sudo pacman -Syu install gcc
conda install pytorch==1.13.1 torchvision==0.14.1 torchaudio==0.13.1 pytorch-cuda=11.7 -c pytorch -c nvidia
pip install "tomli>=2.0.1"
pip install pyngrok

pip install -e .
pip install git+https://github.com/152334H/BigVGAN.git
(Optional) Install ngrok to make the web UI available over the internet:

pip install pyngrok
#ngrok authtoken <your_authtoken>
ngrok http http://localhost:8501 > /dev/null &

#F Launch the web UI and start generating speech 🎉

streamlit run scripts/app.py

#The first start of the web UI will take 5–10 minutes, 
# because all model weights are loaded in the background.
