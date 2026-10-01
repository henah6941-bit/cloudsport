FROM python:3.12-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/alembic.ini .
COPY backend/migrations ./migrations
COPY backend/app ./app
COPY backend/db-init.sh .
RUN sed -i 's/\r$//' /app/db-init.sh && chmod +x /app/db-init.sh
ENV PYTHONPATH=/app
EXPOSE 8000
CMD ["sh", "-c", "./db-init.sh && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
