# MISW-4202-2024-Grupo15-Experimento-Seguridad
Repository for MISW 4202 Agile Software Architectures second experiment, security for software architectures.


## Project Setup
```shell
chmod -R +x "experimentation/"
cd experimentation
./setup.sh
cd ..
```

## Start Project
```shell
cd experimentation
./start_microservices.sh
cd ..
```

you can check the following URLs:
- http://127.0.0.1:7373/docs | Authentication
- http://127.0.0.1:4343/docs | Authorization
- http://127.0.0.1:9393/docs | API Gateway


## Stop Project
```shell
cd experimentation
./stop_microservices.sh
cd ..
```

## Run experiment
Run all the contents in `experimentation/src/stats.ipynb`.
All components must be up. `experimentation/stop_microservices.sh` will remove our DB.
