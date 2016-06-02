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

#### Example
```bash
$ iGen examples/hello.imp | z3 -in
```

#### Tests
```bash
$ iRunTests.sh
```
