FROM python:3.10-alpine

RUN apk update && apk add --no-cache --virtual bash gcc musl-dev linux-headers jpeg-dev zlib-dev mariadb-dev libffi-dev

# copy application directory, keep this commented while using docker-compose.yaml on developer's machine
COPY Ticket_Project /var/www/html
# install pypi packages
COPY ./docker/requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./docker/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh
RUN chmod +x /entrypoint.sh
