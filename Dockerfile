FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY antipe ./antipe
COPY static ./static
COPY pilot ./pilot
RUN useradd --uid 10001 --create-home editor && mkdir -p /app/.local && chown editor:editor /app/.local
USER editor
EXPOSE 8000
CMD ["python", "-m", "antipe", "serve", "--host", "0.0.0.0"]
