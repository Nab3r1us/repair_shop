FROM python:latest

WORKDIR /api
COPY requirements.txt .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]