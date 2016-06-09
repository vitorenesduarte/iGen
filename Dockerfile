FROM ubuntu:14.04
MAINTAINER Vitor Enes Duarte <vitorenesduarte@gmail.com>

# install git python3
RUN apt-get -y update
RUN apt-get -y install build-essential
RUN apt-get -y install git python

# install z3
RUN git clone https://github.com/Z3Prover/z3.git && \
    cd z3/ && \
    python scripts/mk_make.py --python && \
    cd build/ && \
    make && \
    make install

# install pip, simplejson
RUN apt-get -y install python-setuptools && \
    easy_install pip && \
    pip install simplejson

# install iGen
RUN git clone https://github.com/vitorenesduarte/iGen.git #&& \
    cd iGen/ && \
    # run one example
    ./iGen examples/tp.imp 
