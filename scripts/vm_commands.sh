git clone https://github.com/jonheng/brain-opera-gpt2-deployment.git

echo "Copying model into repo folder and setting working directory"
mv model/ brain-opera-gpt2-deployment/model
cd brain-opera-gpt2-deployment/
echo "Present working directory: $PWD"

echo "Installing python3-venv"
sudo apt-get install -y python3-venv

echo "Setting up virtual environment and python dependencies"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

echo "Starting server as a daemon process"
gunicorn -D -b :8000 server:app