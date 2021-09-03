from typing import Union
from pydantic import BaseModel, Field


class Message(BaseModel):
    """ Message model """
    sender: Union[str, int] = Field(max_length=25)
    recipient: Union[str, int] = Field(max_length=25)
    text: str = Field(max_length=140)
