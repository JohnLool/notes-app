FROM python:3.11-slim

RUN apt-get update && apt-get install -y postgresql-client

WORKDIR /app

COPY backend/requirements.txt /app/requirements.txt
COPY entrypoint.sh /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

COPY backend /app

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]