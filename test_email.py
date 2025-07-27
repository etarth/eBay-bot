# test_email.py
from email_notifier import send_email_notification

# Mock data simulating eBay items
mock_items = [
    {
        "title": "Test Vintage Rolex",
        "price": "1999.99",
        "url": "https://www.ebay.com/itm/1234567890"
    },
    {
        "title": "Test Omega Seamaster",
        "price": "899.99",
        "url": "https://www.ebay.com/itm/0987654321"
    }
]

# Send test email
send_email_notification(mock_items)
