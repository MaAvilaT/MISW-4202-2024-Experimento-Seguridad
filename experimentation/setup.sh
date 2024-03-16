#!/bin/bash

# exit on error
function clean_up() {
  rm
}

function install_dependencies() {
  cd "$1"
  python3 -m venv venv
  source venv/bin/activate
  pip install --upgrade pip
  pip install -r requirements.txt
  deactivate
}

install_dependencies "../component-api-gateway"
install_dependencies "../component-authentication"
install_dependencies "../component-authorization"

# KILLS ALL YOUR python3 PROCESSES
# shellcheck disable=SC2046
kill -9 $(ps -a | grep python3 | awk '{print $1}')
