# iGen

[![Build Status](https://travis-ci.org/vitorenesduarte/iGen.svg?branch=master)](https://travis-ci.org/vitorenesduarte/iGen)

### Prerequisites
- Python
- [Z3 Python binding](https://github.com/Z3Prover/z3#python)

```bash
$ python scripts/mk_make.py --python
$ cd build
$ make
```

```bash
$ pip install nose coverage
$ pip install simplejson
```

#### Example
```bash
$ iGen examples/hello.imp | z3 -in
```

#### Tests
```bash
$ iRunTests.sh
```
