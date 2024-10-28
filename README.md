# Getting Started
This guide will help you set up and run the project that represents book library API for basic *CRUD* record's manipulations. The setup script `run.sh` automates the process of creating a database, configuring user credentials, installing dependencies, running migrations, and starting the server.

## Prerequisites 
- **Python 3** and **pip**: Make sure you have Python 3 and pip installed on your system. 
- **PostgreSQL**: Ensure PostgreSQL is installed and running. If not, install it using your package manager (e.g., `sudo apt install postgresql` on Ubuntu).

## Setup instructions

#### Clone the repository:
```
git clone https://github.com/payemo/book-library-management-api.git
cd book-library-management-api
```

#### Run setup script:
Provided script will automate the environment setup and configuration for you. It will:
-   Prompt you for database details (name, user, password, host, and port).
-   Create the PostgreSQL database and user.
-   Set up a virtual environment and install all dependencies.
-   Generate a `.env` file to store database credentials.
-   Apply migrations and run initial tests.
```
chmod +x run.sh
./run.sh
```
## Environment Variables
The `.env` file, stored in the same directory with `settings.py`, created by the script contains the database configuration. Here’s a sample `.env` file that will be created:
```
DATABASE_NAME=<your_database_name>
DATABASE_USER=<your_database_user>
DATABASE_PASSWORD=<your_database_password>
DATABASE_HOST=127.0.0.1
DATABASE_PORT=5432
```