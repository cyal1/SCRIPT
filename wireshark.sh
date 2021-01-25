#!/bin/sh
echo >/tmp/.ssl-key.log
export SSLKEYLOGFILE=/tmp/.ssl-key.log 
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --user-data-dir=/tmp/chrome --ssl-key-log-file=/tmp/.ssl-key.log &
echo $SSLKEYLOGFILE
