# PostgreSQL set-up

## Activate postgres server

When starting the postgres service for the first time, initialize the setup.

```shell
$ sudo /usr/bin/postgresql-setup --initdb
```

Start the postgres service.

```shell
$ sudo service postgresql start
```

Tell postgres to restart each time the server needs to reboot.

```shell
$ sudo systemctl enable postgresql
```

## Create database and users

Using `sudo`, change to the postgres account that was automatically set up when postgres was first initialized.

```shell
$ sudo -i -u postgres
exit
```

As the postgres account, create a new postgres user account.

```shell
$ sudo -u postgres createuser --interactive
>>> User name: spsm-database
>>> Super-user ? : yes
```

As the postgres account, create a new database on the postgres server.

```shell
$ sudo -u postgres createdb spsm-database
```

As `sudo`, create a user with the same name as the postgres user account we created. Assign a password to the user.

```shell
$ sudo adduser spsm-database
$ sudo passwd spsm-database
>>> Changing password for user spsm-database.
>>> New password: ********
```

## Modify authentication configuration

Modify user authentication requirements in `/var/lib/pgsql/data/pg_hba.conf`.

Modify the Python script's configuration details in `src/build-database/config.yml`

```yaml
connection:
  db_name: "spsm-database"
  db_user: "spsm-database"
  db_password: "********"
  db_port: "5432"
  db_host: "localhost"
```

## Test connection

Use the Python script to ingest some data in the database

```shell
$ cd src/build-database/
$ python import_sources.py config.yml condor
```

## GUI

TODO: Open port to allow access to DuckDB.
