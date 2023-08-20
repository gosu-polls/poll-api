FROM python:3.10.6-slim

# Allow statements and log messages to immediately appear in the Cloud Run logs
ENV PYTHONUNBUFFERED 1

WORKDIR /app

EXPOSE 3003

COPY requirements.txt ./

RUN pip install -r requirements.txt

# COPY .env ./
COPY ./app ./

# CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app.main:app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3003"]

# If running behind a proxy like Nginx or Traefik add --proxy-headers
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--proxy-headers"]
