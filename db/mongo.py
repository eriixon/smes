from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Union, List

from bson import ObjectId
from pymongo import MongoClient
from pymongo.collection import Collection

from models.message import Message


@dataclass
class MongoDB:
    """ MongoDB class to retrieve and save data """
    days_limit: int
    messages_limit: int
    _collection: Collection = None

    @property
    def collection(self):
        if not self._collection:
            client = MongoClient("mongodb://localhost:27017")
            db = client['message_db']
            self._collection = db['messages']
            self._collection.delete_one({'_id': self._collection.insert_one({}).inserted_id})
        return self._collection

    def post_message(self, message: Message):
        """
        Save a message in MongoDB
        :param message: message to save
        :return: message id
        """
        return self.collection.insert_one(message.dict()).inserted_id

    def _get_messages(self, params) -> List[dict]:
        """
        Base method to retrieve messages from MongoDB
        :param params: search parameters
        :return: list of messages
        """
        last_day = datetime.now() - timedelta(days=self.days_limit)
        all_params = {**params, **{"_id": {"$gte": ObjectId.from_datetime(last_day)}}}
        return [Message.parse_obj(m).dict() for m in self.collection.find(params).limit(self.messages_limit)]

    def get_all_messages(self) -> List[dict]:
        """
        The method to retrieve all messages from MongoDB
        :param params: search parameters
        :return: list of messages
        """
        return self._get_messages({})

    def get_sender_to_recipient_messages(self, sender: Union[str, int], recipient: Union[str, int]) -> List[dict]:
        """
        The method to retrieve all messages from a sender to a recipient from MongoDB
        :param sender: sender id
        :param recipient: recipient id
        :return: list of messages
        """
        params = {"sender": sender, "recipient": recipient}
        return self._get_messages(params)
