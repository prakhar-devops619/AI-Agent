import requests

SLACK_WEBHOOK_URL = "<YOUR_SLACK_WEBHOOK_URL>"

def send_slack_notification(title, message):
    payload = {
        "text": f"*{title}*\n{message}"
    }
    response = requests.post(SLACK_WEBHOOK_URL, json=payload)
    return response.status_code == 200
