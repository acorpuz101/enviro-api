exec python -m flask run --host=0.0.0.0 >> logs.log &
echo "kill $!" > shutdown.sh
