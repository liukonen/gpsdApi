#!/bin/bash

# Find the process IDs (PIDs) of all running Gunicorn processes
pids=$(pgrep gunicorn)

if [[ -z "$pids" ]]; then
  echo "No Gunicorn processes found."
else
  echo "Found Gunicorn processes with PIDs: $pids"

  # Send termination signal to each Gunicorn process
  for pid in $pids; do
    echo "Stopping Gunicorn process with PID: $pid"
    kill $pid
  done

  echo "All Gunicorn processes stopped."
fi