FROM mcr.microsoft.com/playwright/python:v1.44.0

WORKDIR /app

RUN pip install playwright==1.44.0 && playwright install --with-deps chromium

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY app /app
COPY entrypoint.sh /app
RUN chmod +x /app/entrypoint.sh

EXPOSE 80
ENTRYPOINT ["/app/entrypoint.sh"]
