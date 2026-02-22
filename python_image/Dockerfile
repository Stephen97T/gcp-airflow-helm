FROM python:3.12-slim

ENV PYTHONPATH=/app

WORKDIR /app

COPY requirements.txt /app/requirements.txt
# Filter out airflow and dev packages
RUN grep -v "apache-airflow" requirements.txt | grep -v "pytest" | grep -v "ruff" | grep -v "mypy" > requirements.tmp && \
    pip install --no-cache-dir -r requirements.tmp && \
    rm requirements.tmp

COPY python_image /app/

CMD ["python", "main.py"]