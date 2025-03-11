#!/bin/bash
echo "Setting up VOL Assistant..."
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip -y
pip install -r requirements.txt
echo "Setup Complete! Running VOL..."
python3 vol.py &

