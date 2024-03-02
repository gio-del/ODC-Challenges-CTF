#!/bin/sh

echo "Starting server"
gunicorn --bind 0.0.0.0:5005 main:app
