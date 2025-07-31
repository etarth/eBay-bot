import os

# Email configuration
EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_APP_PASSWORD = os.environ.get("EMAIL_APP_PASSWORD")
RECEIVER_EMAIL = os.environ.get("RECEIVER_EMAIL")

# Search configuration
SEARCH_QUERY = os.environ.get("SEARCH_QUERY", "vintage shirt")
CHECK_INTERVAL = int(os.environ.get("CHECK_INTERVAL", "5"))  # in minutes
RESULT_LIMIT = int(os.environ.get("RESULT_LIMIT", "20"))

# Optional: Add delay between requests to be respectful
REQUEST_DELAY = float(os.environ.get("REQUEST_DELAY", "1.0"))  # seconds between requests