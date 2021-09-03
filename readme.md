#SMES

A simple backend application can support a web-application to enable two users to send short text messages 
to each other, like Facebook Messages app or Google Chat.

1. Requires python3, pip, virtualenv, mongoDB and pytest (for testing)
2. Create an environment `py -m venv .`
4. Install dependencies `pip install -r requirements.txt`
5. Run the app `flask run`

The application will start on `http://127.0.0.1:5000/`

**API endpoints:**

- _GET `/api/messages`_ returns messages from all senders - with a limit of 100 messages or all messages in last 30 days.
- _GET `/api/messages?sender=<id>&recipient=<id>`_ returns recent messages can be requested for a recipient 
   from a specific sender - with a limit of 100 messages or all messages in last 30 days
- _POST `/api/messages`_ take a message object from request and save it in DB

**Message model:**
```json
{
    "sender": "string", 
    "recipient" : "string",
    "text": "string"
}
```
The sender id and recipient id have limit in 25 characters, the text has limit in 140 characters.