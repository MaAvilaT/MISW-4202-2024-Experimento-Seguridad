#!/bin/bash

# shellcheck disable=SC2046
kill -9 $(ps -a | grep python | awk '{print $1}')
kill -9 $(ps -fx | grep src.main | awk '{print $1}')

if ! cd "../component-authentication"
then
  echo "[ERROR] could not cd into component-authentication"
  exit
fi

if rm 'component-authentication.db'
then
  echo "[INFO] component-authentication.db file has been cleaned up"
fi
