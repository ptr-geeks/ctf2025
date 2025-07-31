FROM python:3.11-slim
WORKDIR /app
COPY server.py .
COPY .env .
RUN pip install python-dotenv
CMD ["python", "server.py"]
