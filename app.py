from flask import Flask, request
import requests

app = Flask(__name__)

# Facebook Page Access Token और Verify Token
PAGE_ACCESS_TOKEN = "YOUR_PAGE_ACCESS_TOKEN"  # इसे बाद में सेट करेंगे
VERIFY_TOKEN = "YOUR_VERIFY_TOKEN"  # इसे भी बाद में सेट करेंगे

@app.route('/', methods=['GET'])
def verify():
    # Webhook verification के लिए
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Verification Failed", 403

@app.route('/', methods=['POST'])
def webhook():
    # Incoming messages को प्रोसेस करना
    data = request.get_json()
    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:
                if 'message' in messaging_event:
                    sender_id = messaging_event['sender']['id']  # Sender ID
                    message_text = messaging_event['message'].get('text')  # Message Text
                    send_message(sender_id, f"आपने कहा: {message_text}")
    return "OK", 200

def send_message(recipient_id, message_text):
    """Facebook API का उपयोग करके Reply भेजें"""
    url = f"https://graph.facebook.com/v12.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    headers = {'Content-Type': 'application/json'}
    data = {
        'recipient': {'id': recipient_id},
        'message': {'text': message_text}
    }
    requests.post(url, headers=headers, json=data)

if __name__ == "__main__":
    app.run(debug=True)
