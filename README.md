# Unifi LED
Tool for switching on/off LED of Unifi Devices

## Installation
1. Download requirements:
```
pip3 install requests urllib3
```
2. Configure inside main.py. Example config:
```
ip = "192.168.1.2"
port = "8443"
username = "admin"
password = "password"
```

## Usage

```
python3 main.py on
```
OR
```
python3 main.py off
```

## License

MIT

## Warning
This is just a proof of concept, you probably shouldn't have your credentials in some python file. Please do not use this in a productive environment.

## Contributing

Pull requests are welcomed. If you find some bug - open issue.
