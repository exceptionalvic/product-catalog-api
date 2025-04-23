FROM python:3.10-alpine

RUN mkdir /usr/src/app
WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN apk add --update --virtual .tmp gcc py3-grpcio g++ libc-dev linux-headers \
	&& apk add tcl-dev tiff-dev musl-dev python3-dev postgresql-dev libpq nano libffi-dev py-cffi \
	&& apk add openssl-dev netcat-openbsd coreutils cargo dos2unix postgresql-client openssh-client rustup certbot certbot-nginx gfortran openblas-dev lapack-dev

RUN pip install --upgrade pip
RUN pip install cryptography


COPY ./requirements.txt /usr/src/app/requirements.txt

# add virtualenv
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install -r requirements.txt

# remove temp folder of OS-based installed packages
RUN apk del .tmp

COPY ./entrypoint.sh /usr/src/app/entrypoint.sh


COPY . /usr/src/app/

RUN chmod +x entrypoint.sh


RUN mkdir -p media
RUN mkdir -p staticfiles

RUN chmod -R 755 media
RUN chmod -R 755 staticfiles
RUN chmod +x entrypoint.sh

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
