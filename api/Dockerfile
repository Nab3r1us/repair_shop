from python:latest

WORKDIR /api
COPY requirements.txt /api
RUN pip3 install --upgrade pip -r requirements.txt
COPY . /api
EXPOSE 5000
