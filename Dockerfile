FROM python:3.9

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Default gunicorn parameters: 1 worker, 1 thread
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
