FROM python:3.12-slim

ENV PYTHONPATH=/app

WORKDIR /app

COPY python_image/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY python_image /app/

CMD ["python", "main.py"]