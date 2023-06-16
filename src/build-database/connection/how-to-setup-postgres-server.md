# Running PostgreSQL Server

## Mac OS

### Launch PostgreSQL

```shell
$ brew services start postgresql@14
```

### Enter into PostgreSQL CLI

```shell
$ psql database-name
```

This transforms the prefix on the command line to `postgres=#`.

### Create new user with a password

```
postgres=# CREATE ROLE name WITH LOGIN PASSWORD 'password';
```

### Exit PostgreSQL CLI

```
postgres=# \q
```
