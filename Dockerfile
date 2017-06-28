FROM ubuntu:17.10

RUN mkdir -p /application
WORKDIR /application

RUN apt-get update && \
    apt-get install --yes \
        build-essential \
        python3-dev \
        python3-pip

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY data data 
COPY server.py .
COPY static static
COPY templates templates
COPY model_collection.pkl .

EXPOSE 8080 

CMD ["python3", "server.py"]
