#!/bin/bash
export PYTHONPATH=$PWD/src:$PWD/test:$PWD/imp-interpreter
nosetests imp-interpreter/ test/ -v --with-coverage
