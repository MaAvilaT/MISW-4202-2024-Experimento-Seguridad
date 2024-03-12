# MISW-4202-2024-Grupo15-Experimento-Seguridad
Repository for MISW 4202 Agile Software Architectures second experiment, security for software architectures.


## Dependencies Setup in _component-authentication_
```shell
python3 -m venv venv

source venv/bin/activate

pip install --upgrade pip

pip install -r requirements.txt
```

### Starting the microservice
```shell
uvicorn main:app --reload
```
