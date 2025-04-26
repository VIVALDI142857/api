FROM python:3.10-slim


WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .
RUN chmod +x start.sh
# Expose the port
EXPOSE 50051


CMD ["./start.sh"]