[:var_set('', """
# Compile command
aoikdyndocdsl -s README.src.md -n aoikdyndocdsl.ext.all::nto -g README.md
""")
]\
[:HDLR('heading', 'heading')]\
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
[:toc(beg='next', indent=-1)]

## Set up AoikTraceCall
[:tod()]

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
[:tod()]

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
