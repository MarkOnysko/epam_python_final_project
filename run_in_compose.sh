#!/bin/bash

if [ ! -f flag.txt ]; then

	echo "Applying migrations to database"
	sleep 1
	flask db upgrade

	echo "Populating database with test data"
	sleep 1
	python3 insert_data.py
	touch flag.txt
fi

echo "Running gunicorn..."
sleep 1
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app --access-logfile -