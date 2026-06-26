# Gunicorn configuration for Frontend on Render
import multiprocessing
import os

# Basic settings
bind = f"0.0.0.0:{os.getenv('PORT', 3000)}"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 120
keepalive = 5

# Logging
accesslog = "-"  # stdout
errorlog = "-"   # stderr
loglevel = "info"

# Process naming
proc_name = "frontend-gunicorn"

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL (si Render lo proporciona)
keyfile = os.getenv("KEY_FILE", None)
certfile = os.getenv("CERT_FILE", None)

# Max requests
max_requests = 1000
max_requests_jitter = 100
