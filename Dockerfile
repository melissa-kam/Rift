from python:2.7

RUN mkdir /home/Rift
WORKDIR /home/Rift
ADD requirements.txt /data/requirements.txt
ADD test-requirements.txt /data/test-requirements.txt
RUN pip install -r /data/requirements.txt
RUN pip install -r /data/test-requirements.txt
RUN adduser --disabled-password --gecos '' rift-worker
