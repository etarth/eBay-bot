import os

EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_APP_PASSWORD = os.environ.get("EMAIL_APP_PASSWORD")
RECEIVER_EMAIL = os.environ.get("RECEIVER_EMAIL")
EBAY_OAUTH_TOKEN = os.environ.get("EBAY_OAUTH_TOKEN")
SEARCH_QUERY = os.environ.get("SEARCH_QUERY", "vintage rolex")
CHECK_INTERVAL = int(os.environ.get("CHECK_INTERVAL", "5"))
RESULT_LIMIT = int(os.environ.get("RESULT_LIMIT", "10"))
