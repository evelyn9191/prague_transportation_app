FROM python:3.7-slim-stretch

WORKDIR /app

COPY requirements.txt ./
RUN apt-get update && apt-get install -y g++ gcc libpq-dev --no-install-recommends git &&\
    rm -rf /var/lib/apt/lists/* &&\
    pip install --no-cache-dir -r requirements.txt &&\
    apt-get -y purge g++ gcc &&\
    apt-get -y autoremove

COPY . ./
ENV PYTHONPATH=${PYTHONPATH}:`pwd`

CMD ["python", "run.py"]
