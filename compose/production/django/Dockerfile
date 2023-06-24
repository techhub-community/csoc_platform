FROM python:3.8.5-alpine

RUN apk update && apk add --no-cache gcc musl-dev libffi-dev openssl-dev

RUN pip install --upgrade pip
RUN pip3 install wheel

WORKDIR /app

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

COPY ./compose/production/django/entrypoint.sh /
ENTRYPOINT [ "sh", "/entrypoint.sh" ]
