# CMPE321 Project 3

### Requirements
- MySQL 8.0+
- Python 3.8+
- Django 4.0.4
- Additional requirements are listed in requirements.txt

### Setup

Before running the project first make sure that all requirements are met with running:

`pip install -r requirements.txt`

Then we need to setup environment variables for the DB connections. Create a `.env` file near `settings.py` location.
This file should include environment variables where values should be placed according to description between **""**. Don't use quotation marks or spaces in `.env` file: 

```
MYSQL_HOST="ip_address_of_mysql_server"
MYSQL_USER="username_for_mysql"
MYSQL_PASSWORD="password_for_user"
MYSQL_PORT="mysql_server_port"
MYSQL_DB="mysql_database_name"
```

Example `.env` file:

```
MYSQL_HOST=localhost
MYSQL_USER=testuser
MYSQL_PASSWORD=123456
MYSQL_PORT=3306
MYSQL_DB=TestDB
```
### Running

Following commands should successfully run the server.

```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0:PORT
```

#### Authors:

* Erim Erkin Dogan
* Omer Faruk Sisman
