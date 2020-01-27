# Cartographer CLI

Command line interface to [Cartographer](https://cartographer.io).

Copyright (C) 2019-Present Cartographer Studios Ltd.

Work in progress, subject to change.

## Requirements

- Linux or macOS
- Python 2.7

## Installation

```bash
pip install .
```

## Usage

```bash
# Display help:
$ cartographer --help

# Search the MoRPh map (outputs in GeoJSON):
cartographer feature search mrsMorph \
             --email <MY_EMAIL> \
             --password <MY_PASSWORD>
```

## Configuration

You can create a "credentials" file in `~/.config/cartographer/credentials`
to supply defaults for parameters like `--email` and `--password`.
Here's an example:

```bash
# Filename: ~/.config/cartographer/credentials

[default]
email="<YOUR_EMAIL>"
password="<YOUR_PASSWORD>"
```

You can skip any parameters in the `credentials` file
when you type a command:

```bash
$ cartographer feature search mrsMorph
```

If you have several ways of accessing Cartographer
(e.g. access to multiple workspaces or private servers),
you can add multiple "profiles" to your credentials file:

```bash
# Filename: ~/.config/cartographer/credentials

[default]
email="<YOUR_EMAIL>"
password="<YOUR_PASSWORD>"

[myprofile]
scheme="https"
host="<API_HOSTNAME>"
email="<OTHER_EMAIL>"
password="<OTHER_PASSWORD>"
```

You can switch profiles on the command line using `--profile`:

```bash
$ cartographer --profile myprofile feature search mrsMorph
```
