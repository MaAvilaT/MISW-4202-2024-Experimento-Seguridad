FROM fedora:39

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN dnf update -vy
RUN dnf install libpq-devel python3-devel gcc g++ -vy
RUN pip install psycopg2
RUN pip install --upgrade -r /app/requirements.txt

COPY ./src /app/src

CMD ["source", "venv/bin/activate"]
CMD ["python3", "-m", "src.main"]
