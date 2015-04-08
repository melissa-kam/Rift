#!/bin/bash

start_containers()
{
  sudo docker build -t rift $RIFT_CODE
  sudo docker run --name rift-worker --link rift-db:db --link rift-mq:mq -p 127.0.0.1:8001:8001 -v $RIFT_CODE:/home/Rift rift \
  su -m rift-worker -c "gunicorn -b '0.0.0.0:8001' rift.api.worker.app:application & celery worker -A rift.api.worker.app"
}
stop_containers()
{
  sudo docker kill rift-worker
  sudo docker rm rift-worker
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