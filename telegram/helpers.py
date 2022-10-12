""" Telegram Helpers """
import json
from enum import Enum
from .exception import TelegramException

class TelegramModes(Enum):
  """ Telegram operation modes """
  HTML = 'HTML'
  MARKDOWNV2 = 'MarkdownV2'
  MARKDOWN = 'Markdown'

  def __str__(self):
    """ Readable property """
    return self.value

class TelegramChoice:
  """ Telegram keyboard choice """
  def __init__(self, text, request_contact=False, request_location=False):
    """
    Constructor
    
    Arguments
    ---------
      text              str     required      Text to display in the choice
      request_contact   bool    optional      Request contact information
      request_location  bool    optional      Request location information
    """
    if not isinstance(text, str):
      raise TelegramException(exception=f'text should be str, received {type(text)}')
    if not isinstance(request_contact, bool):
      raise TelegramException(exception=f'request_contact should be bool, received {type(request_contact)}')
    if not isinstance(request_location, bool):
      raise TelegramException(exception=f'request_location should be bool, received {type(request_location)}')

    self.__text = text
    self.__location = request_location
    self.__contact = request_contact

  @property
  def telegram(self):
    """ Value to send to Telegram API """
    return {
      'text': self.__text,
      'request_contact': self.__contact,
      'request_location': self.__location
    }

class TelegramKeyboard:
  """ Telegram Keyboard : Setter """
  __choices = []
  def __init__(self, choices=[]):
    """
      Constructor

      Arguments
      ---------
        choices     list(str)     required      Text of the option
    """
    if not isinstance(choices, (list, tuple)):
      raise TelegramException(exception=f'choices should be list or tuple, received {type(choices)}')

    for i, choice in enumerate(choices):
      if not isinstance(choice, TelegramChoice):
        raise TelegramException(exception=f'choices[{i}] should be a TelegramChoice, received {type(choices[i])}')
    self.__choices = choices

  @property
  def telegram(self):
    """ Readable property """
    choices = []

    for choice in self.__choices:
      choices.append(choice.telegram)

    if len(choices) > 0:
      return {
        'keyboard': [choices],
        'resize_keyboard': True,
        'one_time_keyboard': True
      }
    return {
      'keyboard': [],
      'resize_keyboard': False,
      'one_time_keyboard': False
    }

class TelegramCommand:
  """ Telegram command """
  def __init__(self, text, description):
    """
    Constructor
    
    Arguments
    ---------
      text          str     required    Raw text command, should be 1-32 characters.
      description   str     required    Command description, should be 3-256 characters.
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
      raise TelegramException(exception=f'description must be less than or equals to 256 characters, received {len(description)}')
    if len(description) < 3:
      raise TelegramException(exception=f'description must be greater than or equals to 3 character, received {len(description )}')

    self.__text = text
    self.__description = description

  @property
  def telegram(self):
    """ Value to send to Telegram API """
    return {
      'command': self.__text,
      'description': self.__description
    }

class TelegramCommandsScope(Enum):
  """ Telegram Commands Scope """
  ALL = 'default'
  PRIVATE = 'all_private_chats'
  GROUP = 'all_group_chats'

  def __str__(self):
    """ Readable property """
    return self.value

  @property
  def telegram(self):
    """ Value to send to Telegram API """
    return json.dumps({'type': self.value})
