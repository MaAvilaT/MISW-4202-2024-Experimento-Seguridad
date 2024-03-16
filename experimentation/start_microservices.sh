#!/bin/bash

cd "../component-api-gateway" || exit
source "venv/bin/activate"
python3 -m src.main > api-gateway.log 2>&1 & __api_gateway_pid=$!
deactivate

cd "../component-authentication" || exit
source "venv/bin/activate"
python3 -m src.main > authentication.log 2>&1 & __authentication_pid=$!
deactivate

cd "../component-authorization" || exit
source "venv/bin/activate"
nohup python3 -m src.main > authorization.log 2>&1 & __authorization_pid=$!
deactivate

echo "[INFO] Running component-api-gateway in PID \`${__api_gateway_pid}\`"
echo "[INFO] Running component-authentication in PID \`${__authentication_pid}\`"
echo "[INFO] Running component-authorization in PID \`${__authorization_pid}\`"

echo "[INFO] We will wait for all the processes to finish"

wait "$__api_gateway_pid" "$__authentication_pid" "$__authorization_pid"

# shellcheck disable=SC2046
kill -9 $(ps -a | grep python3 | awk '{print $1}')
