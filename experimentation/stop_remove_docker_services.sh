#!/bin/bash

# shellcheck disable=SC2046
docker image rm -f $(docker images | grep "deployment\|component" | awk '{print $3}')
docker rm -f $(docker ps -a | grep "deployment\|component" | awk '{print $1}')
