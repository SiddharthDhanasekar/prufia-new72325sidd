# Prufia Project

This is the README for setting up and running a Flask application.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have Python and pip installed.
- You have MySQL server installed and running.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/soumyadream96/Prufia.git
   cd Prufia

2. **Install dependencies:**

    Make sure you have pip installed and run the following command:
    ```bash
    pip install -r requirements.txt
    
3. **Set up environment variables:**

    Create a .env file in the root of your project directory with necessary environment variables. An example might look like this:

    ```bash 
    FLASK_APP=run.py
    FLASK_ENV=development
    DATABASE_URL=mysql+pymysql://<username>:<password>@localhost/<database_name>

4. **Start the MySQL Server:**

    Ensure your MySQL server is running. You can typically do this via your terminal, control panel, or service manager depending on your system.

5. **Run the SQL file:**

    Import the prufia.sql file into your MySQL database. This will set up the necessary tables and data. You can do this using the MySQL command line or a database management tool such as phpMyAdmin.

    Example using MySQL command line:
    ```
    mysql -u <username> -p <database_name> < prufia.sql


## Running the Application

Once the setup is complete, start the Flask application using the following command:

    flask run

## Accessing the Application


    http://localhost:5000


You should now see the Flask application running!


    