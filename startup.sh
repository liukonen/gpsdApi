#!/bin/bash
nohup gunicorn -c gunicorn_config.py gps_api:app > log.log 2>&1 &