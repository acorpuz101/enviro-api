PROJECT_DIR=/home/pi/flask-app
export FLASK_APP=$PROJECT_DIR/app.py
exec python -m flask run --host=0.0.0.0 >> $PROJECT_DIR/logs.log &
echo "kill $!" > $PROJECT_DIR/shutdown.sh
