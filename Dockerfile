FROM mcr.microsoft.com/playwright/python:latest

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src /app
COPY ./entrypoint.sh /app
RUN chmod +x ./entrypoint.sh

EXPOSE 80
ENTRYPOINT ["./entrypoint.sh"]
