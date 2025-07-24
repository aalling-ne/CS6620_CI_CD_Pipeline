FROM python:3.11-slim

WORKDIR /app
COPY . .

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y curl

EXPOSE 5000

CMD ["python", "app.py"]