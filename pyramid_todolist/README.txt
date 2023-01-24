Pyramid TodoList
===============================
https://docs.pylonsproject.org/projects/pyramid/en/latest/#getting-started

Getting Started
---------------

- Change directory into your newly created project.

    cd TodoList

- Create a Python virtual environment.

    python3 -m venv env && . env/bin/activate

- Upgrade packaging tools.

    pip3 install --upgrade pip setuptools

- Install requirements for the web application via pip3

    pip3 install -r requirements.txt

- Run your project.

    pserve config.ini


Setting up your PostgreSQL database
-----------------------------------
- Step 1 – Enable PostgreSQL Apt Repository

    sudo apt-get install wget ca-certificates
    wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

    sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" >> /etc/apt/sources.list.d/pgdg.list'

- Step 2 – Install PostgreSQL on Ubuntu

    sudo apt-get update
    sudo apt-get install postgresql postgresql-contrib

- Step 3 – Create User for PostgreSQL

    sudo su - postgres
    psql

    postgres-# CREATE ROLE your_username WITH LOGIN CREATEDB ENCRYPTED PASSWORD 'your_password';
    postgres-# \q

- Step 4 - Create Database for pyramid web app

    su - your_username 
    createdb pyramid_todolist

- Step 5 - Adjust access rights (edit pg_hba.conf)

    vim /etc/postgresql/12/main/pg_hba.conf
    ------
    # "local" is for Unix domain socket connections only
    local   all             all                                     trust
    # IPv4 local connections:
    host    all             all             127.0.0.1/32            trust
    ------

    service postgresql restart

- Step 6 - Initialize database for pyramid web application.

    initdb config.ini

    psql pyramid_todolist
    \dt
