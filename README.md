# plcd - A lightweight PLC uptime monitor

![logo](https://github.com/LibreCS/plcd/blob/stable/assets/logo_ascii.png)

# `$ python3 -m pip install --upgrade plcd`

[Package on PyPI](https://pypi.org/project/plcd/)

![Build Test](https://github.com/LibreCS/plcd/actions/workflows/test-lint.yml/badge.svg) ![Dist Check](https://github.com/LibreCS/plcd/actions/workflows/check-dist.yml/badge.svg) ![Test Build Release Publish](https://github.com/LibreCS/plcd/actions/workflows/tbrp.yml/badge.svg) ![GitHub](https://img.shields.io/github/license/LibreCS/plcd) ![GitHub last commit](https://img.shields.io/github/last-commit/LibreCS/plcd)

## Features
- Uptime detection, monitoring, and logging
- Automatic port sniffing and controller detection

## Requirements
- Python 3.7 or higher `# apt-get install python3`
- Pin 22.04 or higher `# apt-get install python3-pip`
- Network connection to PLC

## Usage
Install using pip:
```bash
$ python3 -m pip install --upgrade plcd
```
Run as a python package:
```bash
$ python3 -m plcd
```

## Supported Controllers
All major PLC protocols, see the [list of controllers](https://github.com/LibreCS/plcd/blob/main/src/plcd/plc-ports.dat) for details

## Build from source
#### Linux/macOS
```bash
git clone https://github.com/LibreCS/plcd
cd plcd
python3 -m pip install --upgrade build
python3 -m build
```

#### Windows
```bash
git clone https://github.com/LibreCS/plcd
cd plcd
py -m pip install --upgrade build
py -m build
```

## Future Features
- Multi-controller monitoring
- Controller state monitoring
- Docker integration for continuous monitoring

## Contributing
This project is written in Python and is a great place to start contributing to open-source. Feel free to check the issues tab or implement your own features.

## Contributors
[cpstrommen](https://github.com/cpstrommen) | [tcun](https://github.com/tcun)
