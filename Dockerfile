FROM python:3.11-slim as base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

FROM base as production

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=15s --retries=5 --start-period=5s CMD wget --quiet --tries=2 --spider http://0.0.0.0:80/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]