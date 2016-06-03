#!/bin/bash
python webserver.py &
echo $! > .WebServerPID
google-chrome http://localhost:8000
