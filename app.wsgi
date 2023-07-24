import sys
import logging

logging.basicConfig(stream=sys.stderr)

sys.path.insert(0, "/var/www/covenant-finance/")
sys.path.insert(0, "/var/www/covenant-finance/venv/lib/python3.10/site-packages")

from app import app as application
