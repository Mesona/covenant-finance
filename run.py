import os
from app import app

#TODO: Better detection than /var/www
def in_aws():
    """Checks if this is running in an AWS environment."""
    for _, val in os.environ.items():
        if "/var/www" in val:
            return True

    return False

if __name__ == "__main__":
    if in_aws():
        print("IN AWS")
        app.run(host="0.0.0.0", port=8000, debug=True)
    else:
        app.run(host="127.0.0.1", port=8000, debug=True)
