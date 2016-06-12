# iGen

[![Build Status](https://travis-ci.org/vitorenesduarte/iGen.svg?branch=master)](https://travis-ci.org/vitorenesduarte/iGen)

## Prerequisites
- Python
- [Z3 Python binding](https://github.com/Z3Prover/z3#python)

```bash
$ python scripts/mk_make.py --python
$ cd build
$ make
```

```bash
$ pip install nose coverage
```

#### Example
```bash
$ iGen examples/hello.imp
```

#### Tests
```bash
$ i-run-tests.sh
```

## What about Docker?

#### Docker Build
```bash
$ docker build -t vitorenesduarte/igen:TAG .
```

#### Docker Run
```bash
$ docker run -d \
             -e PYTHONPATH='iGen/src:iGen/imp-interpreter' \
             -p 8000:8000 \
             vitorenesduarte/igen:TAG \
             python iGen/webserver.py iGen/
```

Or

```bash
$ igen-docker TAG
```
