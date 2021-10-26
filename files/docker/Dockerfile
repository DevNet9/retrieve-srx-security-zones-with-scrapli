FROM python:3.9-alpine

### -------------------------------------------------
### Metadata information
### -------------------------------------------------
LABEL name="juniper-automation-container"
LABEL maintainer="cremsburg@protonmail.com"
LABEL description="Scrapli container to manage Juniper devices"
LABEL license="GPLv3"
LABEL url="https://gitlab.com/cremsburg/juniper-automation-container/container_registry"
LABEL build-date="20211025"

### -------------------------------------------------
### Add XML goodies
### -------------------------------------------------
RUN apk add --update --no-cache g++ gcc libxslt-dev libffi-dev openssh

### -------------------------------------------------
### Change directory to /home/scrapli
### -------------------------------------------------
WORKDIR /home/scrapli

### -------------------------------------------------
### Add and install python packages
### -------------------------------------------------
ADD requirements.txt requirements.txt

RUN pip install -r requirements.txt
