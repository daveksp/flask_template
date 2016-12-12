#!/bin/sh

ps ax | grep -E "(flask_template)" | grep -v 'grep' | awk '{print $1}' | xargs kill -9
sleep 1


export FLASKTEMPLATE_ENV=$1

uwsgi --http 0.0.0.0:8089 --wsgi-file runserver.py --callable app --processes 4 --threads 2 --master --lazy --lazy-apps --honour-stdin
