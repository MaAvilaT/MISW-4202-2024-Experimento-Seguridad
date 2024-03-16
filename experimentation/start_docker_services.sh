#!/bin/bash

docker compose -f "../component-api-gateway/docker-compose.yml" -p "deployment-api-gateway" up -d
docker compose -f "../component-authorization/docker-compose.yml" -p "deployment-authorization" up -d
docker compose -f "../component-authentication/docker-compose.yml" -p "deployment-authentication" up -d
