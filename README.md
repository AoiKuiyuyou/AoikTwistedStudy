# AoikTwistedStudy
Python **Twisted** library study.

Tested working with:
- Python 2.7
- Twisted 16.6.0

Trace call using [AoikTraceCall](https://github.com/AoiKuiyuyou/AoikTraceCall):
- [EchoTCPServerTraceCall.py](/src/EchoTCPServerTraceCall.py)
- [EchoTCPServerTraceCallLogPy2.txt](/src/EchoTCPServerTraceCallLogPy2.txt?raw=True)
- [EchoTCPServerTraceCallNotesPy2.txt](/src/EchoTCPServerTraceCallNotesPy2.txt?raw=True)

## Table of Contents
- [Set up AoikTraceCall](#set-up-aoiktracecall)
  - [Setup via pip](#setup-via-pip)
  - [Setup via git](#setup-via-git)
- [Usage](#usage)
  - [Start server](#start-server)
  - [Send request](#send-request)

## Set up AoikTraceCall
- [Setup via pip](#setup-via-pip)
- [Setup via git](#setup-via-git)

### Setup via pip
Run:
```
pip install git+https://github.com/AoiKuiyuyou/AoikTraceCall
```

### Setup via git
Run:
```
git clone https://github.com/AoiKuiyuyou/AoikTraceCall

cd AoikTraceCall

python setup.py install
```

## Usage
- [Start server](#start-server)
- [Send request](#send-request)

### Start server
Run:
```
python "AoikTwistedStudy/src/EchoTCPServerTraceCall.py" > Log.txt 2>&1
```

### Send request
Run:
```
echo hello| nc 127.0.0.1 8000
```
