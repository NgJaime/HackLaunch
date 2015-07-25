#!/usr/bin/env bash

cp /home/ubuntu/HackLaunch/config/nginx/staging-nginx.conf /etc/nginx/nginx.conf
cp /home/ubuntu/HackLaunch/config/supervisor/staging-hacklaunch.conf /etc/supervisor/conf.d/production-hacklaunch.conf
cp /home/ubuntu/HackLaunch/config/supervisor/staging-supervisord.conf /etc/supervisor/supervisord.conf
