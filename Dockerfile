FROM python:3.6-slim

RUN mkdir -p /opt/app

WORKDIR /opt/app

ARG sourcePath

COPY ${sourcePath}/requirements.txt .
RUN pip install -r requirements.txt

COPY ${sourcePath}/ .

EXPOSE 8080

CMD ["python", "app.py" ]

