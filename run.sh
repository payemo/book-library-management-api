#!bin/bash

VENV_DIR=".venv"

if ! command -v python3 &>/dev/null; then
    echo "Python3 is not installed. Please, install Python3 and try again."
    exit 1
fi

# Check if pip3 is installed
if ! command -v pip3 &>/dev/null; then
    echo "pip3 is not installed. Installing pip3 ..."
    sudo apt update && sudo apt install -y python3-pip
fi

# Create virtual environment if it does not exist.
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment ..."
    python3 -m venv $VENV_DIR
fi

# Activate virtual environment
source $VENV_DIR/bin/activate

# Upgrade pip inside the virtual env
pip install --upgrade pip

# Install required python packages
echo "Installing project dependencies ..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Failed to install requirements. Exiting."
    deactivate
    exit 1
fi

# Apply migrations
echo "Applying database migrations ..."
python manager.py migrate
if [ $? -ne 0 ]; then
    echo "Failed to apply migrations. Exiting"
    deactivate
    exit 1
fi

# Run tests
echo "Running tests ..."
python manager.py test
if [ $? -ne 0 ]; then
    deactivate
    exit 1
fi

# Start the server
python manager.py runserver

# Deactivate the virtual env when server stops
deactivate
