#!/usr/bin/env bash

cp /etc/nginx/nginx.conf /home/ubuntu/HackLaunch/config/nginx/staging-nginx.conf
cp /etc/supervisor/conf.d/staging-hacklaunch.conf /home/ubuntu/HackLaunch/config/supervisor/staging-hacklaunch.conf
cp /etc/supervisor/supervisord.conf /home/ubuntu/HackLaunch/config/supervisor/staging-supervisord.conf
