APPNAME=HackLaunch
APPDIR=/home/ubuntu/$APPNAME/

LOGFILE=$APPDIR'logs/gunicorn.log'
ERRORFILE=$APPFIR'logs/gunicorn-error.log'

NUM_WORKERS=3

ADDRESS=127.0.0.1:8000

cd $APPDIR

source ~/.bashrc
source venv/bin/activate

exec gunicorn wsgi \
-w $NUM_WORKERS \
--bind=$ADDRESS \
--log-level=warning \
--log-file=$LOGFILE 2>>$LOGFILE  1>>$ERRORFILE & \
