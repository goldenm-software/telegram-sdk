"""Telegram SDK"""

import json
import logging
import sys
from datetime import datetime

if sys.version_info >= (3, 11):
  from typing import Self
else:
  from typing_extensions import Self

import zoneinfo

import requests

from .exception import TelegramException
from .helpers import TelegramCommand, TelegramCommandsScope, TelegramKeyboard, TelegramModes

UTC = zoneinfo.ZoneInfo('UTC')
logging.basicConfig(
  format='[%(levelname)s] %(asctime)s @ %(name)s: %(message)s',
  level=logging.INFO,
  handlers=[logging.StreamHandler()],
)

log = logging.getLogger('telegram.sdk')


class TelegramSdk:
  """Telegram Bot SDK"""

  def __init__(self: Self, token: str, host: str = 'https://api.telegram.org') -> None:
    """
    Constructs an instance of the Telegram SDK

    :param token: Bot Token to use (required)
    :type token: str
    :param host: Host to use for the API, defaults to 'https://api.telegram.org' (optional)
    :type host: str

    :raises TelegramException: If the token is not a string or is empty.
    """
    log.debug('Initializing Telegram SDK')
    if not isinstance(token, str):
      raise TelegramException(exception=f'token should be str, received {type(token)}')

    if len(token) < 1:
      raise TelegramException(exception='token should be greater than or equals to 1, received 0')

    self._token = token
    self._host = host
    log.debug('Telegram SDK initialized with base URL w/ token: %s', self.base_url)

  @property
  def base_url(self: Self) -> str:
    """Returns the base URL of the API"""
    return f'{self._host}/bot{self._token}'

  def set_token(self: Self, token: str) -> None:
    """
    Set the token of the bot

    :param token: Token to set
    :type token: str
    """
    if not isinstance(token, str):
      raise TelegramException(exception=f'token should be str, received {type(token)}')

    self._token = token

  @property
  def token(self: Self) -> str:
    """Get the token of the bot"""
    return self._token

  def set_host(self: Self, host: str) -> None:
    """
    Set the host of the API

    :param host: Host to set
    :type host: str
    """
    if not isinstance(host, str):
      raise TelegramException(exception=f'host should be str, received {type(host)}')

    self._host = host

  @property
  def host(self: Self) -> str:
    """Get the host of the API"""
    return self._host

  def send_document(
    self: Self,
    chat_id: str | int,
    document_id: str,
    silent: bool = False,
    caption: str = '',
    mode: TelegramModes = TelegramModes.HTML,
  ) -> tuple[bool, str | int]:
    """
    Send document

    :param chat_id: Chat ID to send the message (required)
    :type chat_id: str | int
    :param document_id: Document ID to send (required)
    :type document_id: str
    :param silent: Indicates if the message will emit a sound or not when received (optional)
    :type silent: bool
    :param caption: Caption to send with the document (optional)
    :type caption: str
    :param mode: Message operation mode (optional)
    :type mode: TelegramModes

    :return: Tuple with the status and message ID or description
    :rtype: tuple[bool, str | int]

    :raises TelegramException: If any of the parameters are not of the expected type or length.
    """
    if not isinstance(document_id, str):
      raise TelegramException(exception=f'document_id should be str, received {type(document_id)}')
    if not isinstance(chat_id, (str, int)):
      raise TelegramException(exception=f'chat_id must be str or int, received {type(chat_id)}')
    if not isinstance(silent, bool):
      raise TelegramException(exception=f'silent must be bool, received {type(silent)}')
    if not isinstance(mode, TelegramModes):
      raise TelegramException(exception=f'mode must be TelegramModes class, received {type(mode)}')
    if len(caption) > 1024:
      raise TelegramException(exception=f'caption should be less than or equals to 1024, received {len(caption)}')

    payload = {
      'chat_id': chat_id,
      'document': document_id,
      'disable_notification': silent,
      'parse_mode': mode.value,
      'caption': caption,
    }
    with requests.post(f'{self.base_url}/sendDocument', payload) as req:
      response = req.json()

    if 'description' in response:
      return response['ok'], response['description']
    return response['ok'], response['result']['message_id']

  def send_sticker(
    self: Self,
    chat_id: str | int,
    sticker: str,
    silent: bool = False,
  ) -> tuple[bool, str | int]:
    """
    Send sticker

    :param chat_id: Chat ID to send the message (required)
    :type chat_id: str | int
    :param sticker: Sticker ID to send (required)
    :type sticker: str
    :param silent: Indicates if the message will emit a sound or not when received (optional)
    :type silent: bool

    :return: Tuple with the status and message ID or description
    :rtype: tuple[bool, str | int]

    :raises TelegramException: If any of the parameters are not of the expected type.
    """
    if not isinstance(sticker, str):
      raise TelegramException(exception=f'sticker should be str, received {type(sticker)}')
    if not isinstance(chat_id, (str, int)):
      raise TelegramException(exception=f'chat_id must be str or int, received {type(chat_id)}')
    if not isinstance(silent, bool):
      raise TelegramException(exception=f'silent must be bool, received {type(silent)}')

    payload = {'chat_id': chat_id, 'sticker': sticker, 'disable_notification': silent}
    log.debug('Sending sticker to %s: %s', chat_id, payload)
    with requests.post(f'{self.base_url}/sendSticker', payload) as req:
      response = req.json()

    if 'description' in response:
      return response['ok'], response['description']
    return response['ok'], response['result']['message_id']

  def send_message(
    self: Self,
    chat_id: str | int,
    message: str,
    mode: TelegramModes = TelegramModes.HTML,
    silent: bool = False,
    reply_id: str | int | None = None,
    disable_preview: bool = False,
    keyboard: TelegramKeyboard | None = None,
  ) -> tuple[bool, str | int]:
    """
    Send a message to a chat (May be a group, channel or user)
    Note: To send a message to a user, that user must start the conversation first. Telegram does not allow
    to send messages to "unknown" users.

    :param chat_id: Chat ID to send the message (required)
    :type chat_id: str | int
    :param message: Message to send, maximum length allowed: 1-4096 characters (required)
    :type message: str
    :param mode: Message operation mode (optional)
    :type mode: TelegramModes
    :param silent: Silent notification (optional)
    :type silent: bool
    :param reply_id: Message ID to reply to (optional)
    :type reply_id: str | int | None
    :param disable_preview: Disable web page preview (optional)
    :type disable_preview: bool
    :param keyboard: Keyboard to send with the message (optional)
    :type keyboard: TelegramKeyboard | None

    :return: Tuple with the status and message ID or description
    :rtype: tuple[bool, str | int]

    :raises TelegramException: If any of the parameters are not of the expected type or length.
    """

    if keyboard is None:
      keyboard = TelegramKeyboard()

    if not isinstance(chat_id, (str, int)):
      raise TelegramException(exception=f'chat_id must be str or int, received {type(chat_id)}')

    if not isinstance(message, str):
      raise TelegramException(exception=f'message must be str, received {type(message)}')

    if len(message) < 1:
      raise TelegramException(exception=f'message should be greater than or equals to 1, received {len(message)}')

    if len(message) > 4096:
      raise TelegramException(exception=f'message should be less than or equals to 4096, received {len(message)}')

    if not isinstance(mode, TelegramModes):
      raise TelegramException(exception=f'mode must be TelegramModes class, received {type(mode)}')

    if not isinstance(silent, bool):
      raise TelegramException(exception=f'silent must be bool, received {type(silent)}')

    if reply_id is not None and not isinstance(reply_id, (str, int)):
      raise TelegramException(exception=f'reply_id must be str or int, received {type(reply_id)}')

    payload = {
      'chat_id': chat_id,
      'text': message,
      'parse_mode': mode.value,
      'disable_notification': silent,
      'disable_web_page_preview': disable_preview,
      'reply_markup': json.dumps(keyboard.telegram),
    }

    if reply_id is not None:
      payload['reply_to_message_id'] = reply_id

    log.debug('Sending message to %s: %s', chat_id, payload)

    with requests.post(f'{self.base_url}/sendMessage', payload) as req:
      response = req.json()

    if 'description' in response:
      return response['ok'], response['description']
    return response['ok'], response['result']['message_id']

  def send_image(
    self: Self,
    chat_id: str | int,
    image_uri: str,
    caption: str | None = None,
  ) -> tuple[bool, str | int]:
    """
    Send image

    :param chat_id: Chat ID to send the message (required)
    :type chat_id: str | int
    :param image_uri: Image URI to send (required)
    :type image_uri: str
    :param caption: Caption to send with the image (optional)
    :type caption: str | None

    :return: Tuple with the status and message ID or description
    :rtype: tuple[bool, str | int]

    :raises TelegramException: If any of the parameters are not of the expected type or length.
    """
    if not isinstance(chat_id, (str, int)):
      raise TelegramException(exception=f'chat_id must be str or int, received {type(chat_id)}')

    if caption is not None:
      if not isinstance(caption, (str, int)):
        raise TelegramException(exception=f'caption must be str or int, received {type(caption)}')
      if len(caption) < 1:
        raise TelegramException(exception=f'caption should be greater than or equals to 1, received {len(caption)}')
      if len(caption) > 1024:
        raise TelegramException(exception=f'caption should be less than or equals to 1024, received {len(caption)}')

    payload = {'chat_id': chat_id, 'photo': image_uri}

    if caption is not None:
      payload['caption'] = caption

    log.debug('Sending image to %s: %s', chat_id, payload)
    with requests.post(f'{self.base_url}/sendPhoto', payload) as req:
      response = req.json()

    if 'description' in response:
      return response['ok'], response['description']
    return response['ok'], response['result']['message_id']

  def send_poll(
    self: Self,
    chat_id: str | int,
    question: str,
    options: list[str],
    anonymous: bool = False,
    silent: bool = False,
    multiple: bool = False,
    close_date: int | None = None,
  ) -> tuple[bool, str | int]:
    """
    Send a poll to a chat (May be a group, channel or user)

    :param chat_id: Chat ID to send the poll (required)
    :type chat_id: str | int
    :param question: Question to ask in the poll, maximum length allowed: 1-300 characters (required)
    :type question: str
    :param options: List of options to choose from, maximum of 10 options (required)
    :type options: list[str]
    :param anonymous: Indicates if the poll is anonymous (optional, default: False)
    :type anonymous: bool
    :param silent: Indicates if the poll will emit a sound or not when received (optional, default: False)
    :type silent: bool
    :param multiple: Indicates if the poll allows multiple answers (optional, default: False)
    :type multiple: bool
    :param close_date: Date when the poll will be closed, in UNIX timestamp format (optional)
    :type close_date: int | None

    :return: Tuple with the status and message ID or description
    :rtype: tuple[bool, str | int]

    :raises TelegramException: If any of the parameters are not of the expected type or length.
    """
    if not isinstance(chat_id, (str, int)):
      raise TelegramException(exception=f'chat_id must be str or int, received {type(chat_id)}')

    if not isinstance(question, str):
      raise TelegramException(exception=f'question must be str, received {type(question)}')

    if len(question) < 1:
      raise TelegramException(exception=f'question should be greater than or equals to 1, received {len(question)}')

    if len(question) > 300:
      raise TelegramException(exception=f'question should be less than or equals to 300, received {len(question)}')

    if not isinstance(options, (list, tuple)):
      raise TelegramException(exception=f'options must be list or tuple, received {type(options)}')

    if len(options) > 10:
      raise TelegramException(exception=f'options must be maximum of 10 options, received {len(options)}')

    if len(options) < 2:
      raise TelegramException(exception=f'options must be at least 2 options, received {len(options)}')

    for i, option in enumerate(options):
      if not isinstance(option, str):
        raise TelegramException(exception=f'option[{i}] must be str, received {type(option)}')

      if len(option) > 100:
        raise TelegramException(
          exception=f'option[{i}] must be less than or equals to 100 characters, received {len(option)}'
        )

      if len(option) < 1:
        raise TelegramException(
          exception=f'option[{i}] must be greater than or equals to 1 character, received {len(option)}'
        )

    if not isinstance(silent, bool):
      raise TelegramException(exception=f'silent must be bool, received {type(silent)}')

    if not isinstance(anonymous, bool):
      raise TelegramException(exception=f'anonymous must be bool, received {type(anonymous)}')

    if not isinstance(multiple, bool):
      raise TelegramException(exception=f'multiple must be bool, received {type(multiple)}')

    if close_date is not None:
      if not isinstance(close_date, int):
        raise TelegramException(exception=f'close_date must be int, received {type(close_date)}')

      now = datetime.now(UTC).timestamp()
      if now >= close_date:
        raise TelegramException(exception=f'close_date must be greater than {now}, received {close_date}')

    payload = {
      'chat_id': chat_id,
      'question': question,
      'options': json.dumps(options),
      'disable_notification': silent,
      'is_anonymous': anonymous,
      'allows_multiple_answers': multiple,
    }

    if close_date is not None:
      payload['close_date'] = close_date

    log.debug('Sending poll to %s: %s', chat_id, payload)
    with requests.post(f'{self.base_url}/sendPoll', payload) as req:
      response = req.json()

    if 'description' in response:
      return response['ok'], response['description']
    return response['ok'], response['result']['message_id']

  def stop_poll(
    self: Self,
    chat_id: str | int,
    poll_id: str | int,
  ) -> tuple[bool, str | int]:
    """
    Stop poll

    :param chat_id: Chat ID where the poll is (required)
    :type chat_id: str | int
    :param poll_id: Poll ID to stop (required)
    :type poll_id: str | int

    :return: Tuple with the status and poll ID or description
    :rtype: tuple[bool, str | int]

    :raises TelegramException: If any of the parameters are not of the expected type.
    """
    if not isinstance(chat_id, (str, int)):
      raise TelegramException(exception=f'chat_id must be str or int, received {type(chat_id)}')
    if not isinstance(poll_id, (str, int)):
      raise TelegramException(exception=f'poll_id must be str or int, received {type(poll_id)}')

    payload = {'chat_id': chat_id, 'message_id': poll_id}

    log.debug('Stopping poll in %s: %s', chat_id, payload)
    with requests.post(f'{self.base_url}/stopPoll', payload) as req:
      response = req.json()

    if 'description' in response:
      return response['ok'], response['description']
    return response['ok'], response['result']['id']

  def get_file(
    self: Self,
    file_id: str,
  ) -> tuple[bool, str]:
    """
    Get a file from API

    :param file_id: File ID to get (required)
    :type file_id: str

    :return: Tuple with the status and file path or description
    :rtype: tuple[bool, str]

    :raises TelegramException: If file_id is not a string.
    """

    if not isinstance(file_id, str):
      raise TelegramException(exception=f'file_id should be str, received {type(file_id)}')

    payload = {'file_id': file_id}

    log.debug('Getting file from %s: %s', self.host, payload)
    with requests.post(f'{self.base_url}/getFile', payload) as req:
      response = req.json()

    if 'description' in response:
      return response['ok'], response['description']
    return response['ok'], response['result']['file_path']

  def set_commands(
    self: Self,
    commands: list[TelegramCommand],
    scope: TelegramCommandsScope = TelegramCommandsScope.ALL,
    language: str | None = None,
  ) -> tuple[bool, str | int]:
    """
    Set the commands list for the bot

    :param commands: List of commands to set (required)
    :type commands: list[TelegramCommand]
    :param scope: Scope of the commands (optional, default: TelegramCommandsScope.ALL)
    :type scope: TelegramCommandsScope
    :param language: Locale or Language locale of the commands list (optional)
    :type language: str | None

    :return: Tuple with the status and description or result
    :rtype: tuple[bool, str | int]

    :raises TelegramException: If commands is not a list or tuple, if any command is not a TelegramCommand,
    """

    if not isinstance(commands, (list, tuple)):
      raise TelegramException(exception=f'commands must be list or tuple, received {type(commands)}')

    for i, command in enumerate(commands):
      if not isinstance(command, TelegramCommand):
        raise TelegramException(exception=f'command[{i}] must be a TelegramCommand, received {type(command)}')

    if not isinstance(scope, TelegramCommandsScope):
      raise TelegramException(exception=f'scope must be TelegramCommandsScope, received {type(scope)}')

    if language is not None:
      if not isinstance(language, str):
        raise TelegramException(exception=f'language must be str, received {type(language)}')

      if len(language) != 2:
        raise TelegramException(exception='language must be a 2 character ISO 639-1 code')

    parsed_commands = []

    for command in commands:
      parsed_commands.append(command.telegram)

    payload = {'commands': json.dumps(parsed_commands), 'scope': scope.telegram}

    if language is not None:
      payload['language_code'] = language

    log.debug('Setting commands: %s', payload)
    with requests.post(f'{self.base_url}/setMyCommands', payload) as req:
      response = req.json()

    if 'description' in response:
      return response['ok'], response['description']
    return response['ok'], response['result']

  def delete_commands(
    self: Self,
    scope: TelegramCommandsScope = TelegramCommandsScope.ALL,
    language: str | None = None,
  ) -> tuple[bool, str | int]:
    """
    Delete current commands

    :param scope: Scope of the commands (optional, default: TelegramCommandsScope.ALL)
    :type scope: TelegramCommandsScope
    :param language: Locale or Language locale of the commands list (optional)
    :type language: str | None

    :return: Tuple with the status and description or result
    :rtype: tuple[bool, str | int]

    :raises TelegramException: If scope is not a TelegramCommandsScope, if language is not a string or if it is not
    a 2 character ISO 639-1 code.
    """
    if not isinstance(scope, TelegramCommandsScope):
      raise TelegramException(exception=f'scope must be TelegramCommandsScope, received {type(scope)}')

    if language is not None:
      if not isinstance(language, str):
        raise TelegramException(exception=f'language must be str, received {type(language)}')

      if len(language) != 2:
        raise TelegramException(exception='language must be a 2 character ISO 639-1 code')

    payload = {'scope': scope.telegram}

    if language is not None:
      payload['language_code'] = language

    log.debug('Deleting commands: %s', payload)
    with requests.post(f'{self.base_url}/deleteMyCommands', payload) as req:
      response = req.json()

    if 'description' in response:
      return response['ok'], response['description']
    return response['ok'], response['result']

  def leave_chat(
    self: Self,
    chat_id: str | int,
  ) -> bool:
    """
    Leave Chat

    :param chat_id: Chat ID to leave (required)
    :type chat_id: str | int

    :return: True if the bot left the chat, False otherwise
    :rtype: bool
    """
    if not isinstance(chat_id, (str, int)):
      raise TelegramException(exception=f'chat_id must be str or int, received {type(chat_id)}')

    log.debug('Leaving chat %s', chat_id)
    with requests.post(f'{self.base_url}/leaveChat', {'chat_id': chat_id}) as req:
      response = req.json()

    return response['ok']

  def set_webhook(self: Self, uri: str) -> bool:
    """
    Set Webhook

    :param uri: URI to set as webhook (required)
    :type uri: str

    :return: True if the webhook was set successfully, False otherwise
    :rtype: bool
    """
    if not isinstance(uri, str):
      raise TelegramException(exception=f'uri must be str, received {type(uri)}')

    payload = {'url': uri, 'allowed_updates': ['message', 'edited_message'], 'drop_pending_updates': True}

    log.debug('Setting webhook: %s', payload)
    with requests.post(f'{self.base_url}/setWebhook', payload) as req:
      response = req.json()

    return response['ok']

  def delete_webhook(self: Self) -> bool:
    """
    Delete Webhook

    :return: True if the webhook was deleted successfully, False otherwise
    :rtype: bool
    """

    log.debug('Deleting webhook')
    with requests.post(f'{self.base_url}/deleteWebhook') as req:
      response = req.json()

    return response['ok']


__all__ = ['TelegramSdk']
