bind = '127.0.0.1:9999'  # Specify the host and port for Gunicorn to bind to
workers = 3  # The number of Gunicorn worker processes to spawn
loglevel = 'info'  # Log level for Gunicorn logs
#errorlog = '-'  # Log file for Gunicorn errors (use '-' for stdout)
#accesslog = '-'  # Log file for Gunicorn access logs (use '-' for stdout)