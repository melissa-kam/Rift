#!/bin/bash

start_containers()
{
  docker build -t rift $RIFT_CODE
  docker run --name rift-api --link rift-mq:mq --link rift-db:db  -p 127.0.0.1:8000:8000 -v $RIFT_CODE:/home/Rift rift \
  gunicorn -b '0.0.0.0:8000' rift.app:application
}
stop_containers()
{
  docker kill rift-api
  docker rm rift-api
}

if [[ -z $RIFT_CODE ]]; then
    echo "Need to set RIFT_CODE."
    exit 1
fi

case "$1" in
  start)
    start_containers
    ;;
  stop)
    stop_containers
    ;;
  restart)
    stop_containers
    start_containers
    ;;
  *)
    echo "Usage: rift_worker.sh {start|stop|restart}"
    exit 1
esac
