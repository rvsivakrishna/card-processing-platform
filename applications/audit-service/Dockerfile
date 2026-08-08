FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt && \
    useradd --create-home --shell /usr/sbin/nologin audituser

COPY --chown=audituser:audituser app.py .

USER audituser

EXPOSE 8082

CMD ["gunicorn", "--bind", "0.0.0.0:8082", "--workers", "2", "--access-logfile", "-", "app:app"]
