FROM python:3.11-slim

WORKDIR /app

# Install required packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY templates/ templates/
COPY static/ static/

# Create non-root user
RUN useradd -m -u 1000 ctfuser
RUN chown -R ctfuser:ctfuser /app
USER ctfuser

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

EXPOSE 5000

CMD ["python", "app.py"]
