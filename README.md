# plcd - A lightweight PLC uptime monitor

![logo](assets/logo_ascii.png)

# `$ pip install plcd`

## Requirements
- Python 3.7 or higher `# apt-get install python3`
- Pin 22.04 or higher `# apt-get install python3-pip`
- Network connection to PLC

## Supported Controllers
- Siemens
- Allen-Bradley Rockwell (Modern)

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
- Port sniffing and automatic detection
- Multi-controller monitoring
- Controller state monitoring
- Docker integration for continuous monitoring

## Contributing
This project is written in Python and is a great place to start contributing to open-source. Feel free to check the issues tab or implement your own features.

## Contributors