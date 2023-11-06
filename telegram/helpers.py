""" Telegram Helpers """
import json
from enum import Enum

from .exception import TelegramException


class TelegramModes(Enum):
  """ Telegram operation modes """
  HTML = 'HTML'
  MARKDOWNV2 = 'MarkdownV2'
  MARKDOWN = 'Markdown'

  def __str__(self) -> str:
    """ Readable property """
    return self.value


class TelegramChoice:
  """ Telegram keyboard choice """

  def __init__(
    self,
    text: str,
    request_contact: bool = False,
    request_location: bool = False,
  ):
    """
    Constructor
    ---
    Arguments
      - text: Text to display in the choice button (required)
      - request_contact: Request contact information (optional)
      - request_location: Request location information (optional)
    """
    if not isinstance(text, str):
      raise TelegramException(exception=f'text should be str, received {type(text)}')
    if not isinstance(request_contact, bool):
      raise TelegramException(exception=f'request_contact should be bool, received {type(request_contact)}')
    if not isinstance(request_location, bool):
      raise TelegramException(exception=f'request_location should be bool, received {type(request_location)}')

    self._text = text
    self._location = request_location
    self._contact = request_contact

  @property
  def telegram(self) -> dict:
    """ Value to send to Telegram API """
    return {'text': self._text, 'request_contact': self._contact, 'request_location': self._location}


class TelegramKeyboard:
  """ Telegram Keyboard """

  def __init__(self, choices: list[str] = []):  # pylint: disable=dangerous-default-value
    """
    Constructor
    ---
    Arguments
      - choices: Text of the option (required)
    """
    if not isinstance(choices, (list, tuple)):
      raise TelegramException(exception=f'choices should be list or tuple, received {type(choices)}')

    for i, choice in enumerate(choices):
      if not isinstance(choice, TelegramChoice):
        raise TelegramException(exception=f'choices[{i}] should be a TelegramChoice, received {type(choices[i])}')
    self._choices: list[str] = choices

  @property
  def telegram(self) -> dict:
    """ Value to send to Telegram API """
    choices = []

    for choice in self._choices:
      choices.append(choice.telegram)

    if len(choices) > 0:
      return {'keyboard': [choices], 'resize_keyboard': True, 'one_time_keyboard': True}
    return {'keyboard': [], 'resize_keyboard': False, 'one_time_keyboard': False}


class TelegramCommand:
  """ Telegram command """

  def __init__(
    self,
    text: str,
    description: str,
  ):
    """
    Constructor
    ---
    Arguments
      - text: Raw text command, should be 1-32 characters. (required)
      - description: Command description, should be 3-256 characters. (required)
    """
    if not isinstance(text, str):
      raise TelegramException(exception=f'text must be str, received {type(text)}')
    if len(text) > 32:
      raise TelegramException(exception=f'text must be less than or equals to 32 characters, received {len(text)}')
    if len(text) < 1:
      raise TelegramException(exception=f'text must be greater than or equals to 1 character, received {len(text)}')
    if not isinstance(description, str):
      raise TelegramException(exception=f'description must be str, received {type(description)}')
    if len(description) > 256:
      raise TelegramException(exception='description must be less than or equals to 256 characters, ' +\
                                        f'received {len(description)}')
    if len(description) < 3:
      raise TelegramException(exception='description must be greater than or equals to 3 character, ' +\
                                        f'received {len(description)}')

    self._text: str = text
    self._description: str = description

  @property
  def telegram(self) -> dict:
    """ Value to send to Telegram API """
    return {'command': self._text, 'description': self._description}


class TelegramCommandsScope(Enum):
  """ Telegram Commands Scope """
  ALL = 'default'
  PRIVATE = 'all_private_chats'
  GROUP = 'all_group_chats'

  def __str__(self) -> str:
    """ Readable property """
    return self.value

  @property
  def telegram(self) -> dict:
    """ Value to send to Telegram API """
    return json.dumps({'type': self.value})
