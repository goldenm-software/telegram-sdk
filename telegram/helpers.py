"""Telegram Helpers"""

import json
import sys
from enum import Enum
from typing import Any

if sys.version_info >= (3, 11):
  from typing import Self
else:
  from typing_extensions import Self

from .exception import TelegramException


class TelegramModes(Enum):
  """Telegram operation modes"""

  HTML = 'HTML'
  MARKDOWNV2 = 'MarkdownV2'
  MARKDOWN = 'Markdown'

  def __str__(self: Self) -> str:
    """Readable property"""
    return self.value


class TelegramChoice:
  """Telegram keyboard choice"""

  def __init__(self: Self, text: str, request_contact: bool = False, request_location: bool = False) -> None:
    """
    Constructor

    :param text: Text of the option, should be 1-64 characters. (required)
    :type text: str
    :param request_contact: If True, the user will be able to send their contact information. (optional)
    :type request_contact: bool
    :param request_location: If True, the user will be able to send their location. (optional)
    :type request_location: bool

    :raises TelegramException: If any of the parameters are not of the expected type or length.
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
  def telegram(self: Self) -> dict[str, Any]:
    """
    Value to send to Telegram API

    :return: Dictionary with the text, request_contact, and request_location
    :rtype: dict[str, Any]
    """
    return {'text': self._text, 'request_contact': self._contact, 'request_location': self._location}


class TelegramKeyboard:
  """Telegram Keyboard"""

  def __init__(self, choices: list[TelegramChoice] | tuple[TelegramChoice] | None = None) -> None:
    """
    Constructor

    :param choices: List of TelegramChoice objects. (optional)
    :type choices: list[str] | None
    :raises TelegramException: If choices is not a list or tuple, or if any choice is not a TelegramChoice.
    """
    if choices is None:
      choices = []

    if not isinstance(choices, (list, tuple)):
      raise TelegramException(exception=f'choices should be list or tuple, received {type(choices)}')

    for i, choice in enumerate(choices):
      if not isinstance(choice, TelegramChoice):
        raise TelegramException(exception=f'choices[{i}] should be a TelegramChoice, received {type(choices[i])}')

    self._choices: list[TelegramChoice] | tuple[TelegramChoice] = choices

  @property
  def telegram(self: Self) -> dict[str, Any]:
    """
    Value to send to Telegram API

    :return: Dictionary with the keyboard layout
    :rtype: dict[str, Any]
    """
    choices = []

    for choice in self._choices:
      choices.append(choice.telegram)

    if len(choices) > 0:
      return {'keyboard': [choices], 'resize_keyboard': True, 'one_time_keyboard': True}
    return {'keyboard': [], 'resize_keyboard': False, 'one_time_keyboard': False}


class TelegramCommand:
  """Telegram command"""

  def __init__(self: Self, text: str, description: str) -> None:
    """
    Constructor

    :param text: Command text, should be 1-32 characters. (required)
    :type text: str
    :param description: Description of the command, should be 3-256 characters. (required)
    :type description: str

    :raises TelegramException: If text or description are not of the expected type or length.
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
      raise TelegramException(
        exception='description must be less than or equals to 256 characters, ' + f'received {len(description)}'
      )
    if len(description) < 3:
      raise TelegramException(
        exception='description must be greater than or equals to 3 character, ' + f'received {len(description)}'
      )

    self._text: str = text
    self._description: str = description

  @property
  def telegram(self: Self) -> dict[str, str]:
    """
    Value to send to Telegram API

    :return: Dictionary with the command and description
    :rtype: dict[str, str]
    """
    return {'command': self._text, 'description': self._description}


class TelegramCommandsScope(Enum):
  """Telegram Commands Scope"""

  ALL = 'default'
  PRIVATE = 'all_private_chats'
  GROUP = 'all_group_chats'

  def __str__(self: Self) -> str:
    """Readable property"""
    return self.value

  @property
  def telegram(self: Self) -> str:
    """Value to send to Telegram API"""
    return json.dumps({'type': self.value})


__all__ = [
  'TelegramModes',
  'TelegramChoice',
  'TelegramKeyboard',
  'TelegramCommand',
  'TelegramCommandsScope',
]
