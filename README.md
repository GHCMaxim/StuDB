# StuDB

A simple database system project using PyMSSQL.

## Requirements

-   Python 3.10+
-   Dependencies: `python-pipenv`, `typing_extensions`, `option`, `pymssql`, `flask`, `flask-restful`
-   MSSQL

## Usage

### pipenv

This repository uses `pipenv` to manage its dependancies and Python interpreter. If you haven't installed `pipenv`:

```
$ pip install --user pipenv
```

Afterwards, a virtual environment can be setup by running:

```
$ pipenv install
```

Everything else can be ran using the environment managed by `pipenv`:

```
$ pipenv run <command>
```

### Actual usage

Please fill out the `.env` file using `.env_example` as a base.

Afterwards, run:

```
$ pipenv run python main_tui.py
```
or

```
$ pnpm start
```

to start the program.

## Contribution

Please follow the [Contribution Guide](CONTRIBUTING.md) to develop.
