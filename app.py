from flask import Flask, request, jsonify, Response
from models.message import Message
from db.mongo import MongoDB

days_limit: int = 30
messages_limit: int = 100

app = Flask(__name__)
db = MongoDB(days_limit, messages_limit)


@app.route('/api/messages', methods=["GET"])
def get_all_messages():
    """
    Retrieve messages from DB
    :return: HTTP response
    """
    try:
        sender = request.args['sender']
        recipient = request.args['recipient']
    except KeyError:
        messages = db.get_all_messages()
    else:
        messages = db.get_sender_to_recipient_messages(sender, recipient)

    if messages:
        return jsonify(messages)

    return Response(status=404, response='no messages found')


@app.route('/api/messages', methods=["POST"])
def post_message():
    """
    Save messages into DB
    :return: HTTP response
    """
    message = Message.parse_obj(request.get_json(force=True))
    if db.post_message(message):
        return Response(status=201)
    return Response(status=500, response='message is not saved')
