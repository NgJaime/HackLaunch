#!/usr/bin/env bash

cp /home/ubuntu/HackLaunch/config/nginx/nginx.conf /etc/nginx/nginx.conf
cp /home/ubuntu/HackLaunch/config/supervisor/production-hacklaunch.conf /etc/supervisor/conf.d/production-hacklaunch.conf
cp /home/ubuntu/HackLaunch/config/supervisor/supervisord.conf /etc/supervisor/supervisord.conf
