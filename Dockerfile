FROM python:3.11-alpine as builder

RUN adduser -D nonroot
USER nonroot

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

FROM python:3.11-alpine

COPY --from=builder /app /app

USER nonroot
WORKDIR /app

COPY . .

EXPOSE 80

ENV PYTHONUNBUFFERED 1

HEALTHCHECK --interval=30s --timeout=15s --retries=5 --start-period=5s CMD wget --quiet --tries=2 --spider http://0.0.0.0:80/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]