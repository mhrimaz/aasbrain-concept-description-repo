FROM python:3.11-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 80
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
HEALTHCHECK --interval=30s --timeout=15s --retries=5 --start-period=5s CMD wget --quiet --tries=2 --spider http://0.0.0.0:80/health || exit 1