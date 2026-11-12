FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir flask
COPY . .
EXPOSE 8090 5091
CMD ["python", "app.py"]