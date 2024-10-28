#!/bin/bash

read -p "Enter the database name: " DB_NAME
read -p "Enter the database user: " DB_USER
echo "Enter the password for '$DB_USER': "
read -s DB_PASSWORD
read -p "Enter the database host (default is 127.0.0.1): " DB_HOST
DB_HOST=${DB_HOST:-127.0.0.1} # Default to 127.0.0.1 if left blank
read -p "Enter the database port (default is 5432): " DB_PORT
DB_PORT=${DB_PORT:-5432}

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

# Check if PostgreSQL is installed
if ! command -v psql &>/dev/null; then
    echo "PostgreSQL is not installed. Please install and try again."
    exit 1
fi

# Create PostgreSQL database and user
echo "Setting up PostgreSQL and user ..."
sudo -u postgres psql -c "CREATE DATABASE $DB_NAME;"
sudo -u postgres psql -c "CREATE ROLE $DB_USER WITH SUPERUSER LOGIN PASSWORD '$DB_PASSWORD';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"

echo "Creating .env file for storing database secrets ..."
cd blms
cat <<EOF > .env
DATABASE_NAME=$DB_NAME
DATABASE_USER=$DB_USER
DATABASE_PASSWORD=$DB_PASSWORD
DATABASE_HOST=$DB_HOST
DATABASE_PORT=$DB_PORT
EOF

cd ..

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
python manage.py migrate
if [ $? -ne 0 ]; then
    echo "Failed to apply migrations. Exiting."
    deactivate
    exit 1
fi

# Run tests
echo "Running tests ..."
python manage.py test
if [ $? -ne 0 ]; then
    deactivate
    exit 1
fi

# Start the server
python manage.py runserver

# Deactivate the virtual env when server stops
deactivate
