#!/bin/bash
python webserver.py &
echo $! > .WebServerPID
