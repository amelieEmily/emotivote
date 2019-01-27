#!/usr/bin/env bash

set -xe
ngrok http 5000 -bind-tls=true -config /opt/config/ngrok.yaml -log=stdout > /dev/null &
sleep 5
python emotebot.py &
bash
