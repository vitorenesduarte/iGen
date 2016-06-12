#!/bin/bash
export PYTHONPATH=$PWD/src:$PWD/test:$PWD/imp-interpreter
nosetests --cover-package=src/ --cover-package=imp-interpreter/ -v --with-coverage --cover-erase --cover-html 
google-chrome cover/index.html
