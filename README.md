# StuDB

A simple database system project using PyMSSQL.
## Members
| Username   | Name                           |
| ---------- | ------------------------------ |
| GHCMaxim   | Phan Huy Hiep - 20210328       |
| hacaothu.3 | Cao Thị Thu Hà - 20215271      |
| namkhanh03 | Đặng Trần Nam Khánh - 20215278 |


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

Afterwards, run this command for TUI:

```
$ pipenv run python main_tui.py
```
or this command for web:

```
$ pnpm start
```

to start the program.

## Contribution

Please follow the [Contribution Guide](CONTRIBUTING.md) to develop.
