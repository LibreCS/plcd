# plcd - A lightweight PLC uptime monitor

![logo](assets/logo_ascii.png)

# `$ pip install plcd`

![Build Test](https://github.com/LibreCS/plcd/actions/workflows/test.yml/badge.svg) ![Release](https://github.com/LibreCS/plcd/actions/workflows/release.yml/badge.svg)

## Features
- Uptime detection, monitoring, and logging
- Automatic port sniffing and controller detection

## Requirements
- Python 3.7 or higher `# apt-get install python3`
- Pin 22.04 or higher `# apt-get install python3-pip`
- Network connection to PLC

## Supported Controllers
All major PLC protocols, see the [list of controllers](https://github.com/LibreCS/plcd/blob/main/src/plcd/plc-ports.dat) for details

## Build from source
#### Linux/macOS
```bash
cd plcd
python3 -m pip install --upgrade build
python3 -m build
```

#### Windows
```bash
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
