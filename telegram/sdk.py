""" Telegram SDK """
import json
import logging
from datetime import datetime

import requests

from .exception import TelegramException
from .helpers import (TelegramCommand, TelegramCommandsScope, TelegramKeyboard, TelegramModes)

logging.basicConfig(
  format='[%(levelname)s] %(asctime)s @ %(name)s: %(message)s',
  level=logging.INFO,
  handlers=[logging.StreamHandler()],
)

log = logging.getLogger('telegram.sdk')


class TelegramSdk:
  """ Telegram Bot SDK """

  def __init__(self, token: str, host: str = 'https://api.telegram.org'):
    """ constructor """
    log.debug('Initializing Telegram SDK')
    self._token = token
    self._host = host
    log.debug('Telegram SDK initialized with base URL w/ token: %s', self.base_url)

  @property
  def base_url(self) -> str:
    """
    Returns the base URL of the API
    """
    return f'{self._host}/bot{self._token}'

  def set_token(self, token: str) -> None:
    """
    Set the token of the bot
    ---
    Arguments
      - token: Token to set
    """
    if not isinstance(token, str):
      raise TelegramException(exception=f'token should be str, received {type(token)}')

    self._token = token

  @property
  def token(self) -> str:
    """
    Get the token of the bot
    """
    return self._token

  def set_host(self, host: str) -> None:
    """
    Set the host of the API
    ---
    Arguments
      - host: Host to set
    """
    if not isinstance(host, str):
      raise TelegramException(exception=f'host should be str, received {type(host)}')

    self._host = host

  @property
  def host(self) -> str:
    """
    Get the host of the API
    """
    return self._host

  def send_sticker(
    self,
    chat_id: str | int,
    sticker: str,
    silent: bool = False,
  ) -> tuple[bool, str | int]:
    """
    Send sticker
    ---
    Arguments
      - chat_id: Chat ID to send the message (required)
      - sticker: Sticker ID to send (required)
      - silent: Indicates if the message will emit a sound or not when received (optional)
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
      self,
      chat_id: str | int,
      message: str,
      mode: TelegramModes = TelegramModes.HTML,
      silent: bool = False,
      reply_id: str | int = None,
      disable_preview: bool = False,
      keyboard: TelegramKeyboard = TelegramKeyboard(),
  ) -> tuple[bool, str | int]:
    """
      Send a message to a chat (May be a group, channel or user)
      Note: To send a message to a user, that user must start the conversation first. Telegram does not allow
      to send messages to "unknown" users.
      ---
      Arguments
        - chat_id: Chat ID to send the message (required)
        - message: Message to send, maximum length allowed: 1-4096 characters (required)
        - mode: Message operation mode (optional)
        - silent: Indicates if the message will emit a sound or not when received (optional)
        - reply_id: Message ID to reply (optional)
        - keyboard: An instance of TelegramKeyboard with choices, empty by default. (optional)
    """

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
      'reply_markup': json.dumps(keyboard.telegram)
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
    self,
    chat_id: str | int,
    image_uri: str,
    caption: str = None,
  ) -> tuple[bool, str | int]:
    """
    Send image
    ---
    Arguments
      - chat_id: Chat ID to send the message (required)
      - image_uri: Image URI to send (required)
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
    self,
    chat_id: str | int,
    question: str,
    options: list[str],
    anonymous: bool = False,
    silent: bool = False,
    multiple: bool = False,
    close_date: int = None,
  ) -> tuple[bool, str | int]:
    """
    Send a poll to a chat (May be a group, channel or user)
    ---
    Arguments
      - chat_id: Chat ID to send the message (required)
      - question: Question to send, maximum length allowed: 1-300 characters (required)
      - options: Choices to select (required)
      - anonymous: Indicates if the poll could be submitted as Anonymous. (optional)
      - silent: Silent notification (optional)
      - multiple: Allow to submit multiple choices. (optional)
      - close_date: Set the expiration date of the poll (In Unix Timestamp) (optional)
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
          exception=f'option[{i}] must be less than or equals to 100 characters, received {len(option)}')

      if len(option) < 1:
        raise TelegramException(
          exception=f'option[{i}] must be greater than or equals to 1 character, received {len(option)}')

    if not isinstance(silent, bool):
      raise TelegramException(exception=f'silent must be bool, received {type(silent)}')

    if not isinstance(anonymous, bool):
      raise TelegramException(exception=f'anonymous must be bool, received {type(anonymous)}')

    if not isinstance(multiple, bool):
      raise TelegramException(exception=f'multiple must be bool, received {type(multiple)}')

    if close_date is not None:
      if not isinstance(close_date, int):
        raise TelegramException(exception=f'close_date must be int, received {type(close_date)}')

      now = datetime.now().timestamp()
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
    self,
    chat_id: str | int,
    poll_id: str | int,
  ) -> tuple[bool, str | int]:
    """
    Stop poll
    ---
    Arguments
      - chat_id: Chat ID where Poll is submitted (required)
      - poll_id: Message ID where poll is submitted (required)
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
    self,
    file_id: str,
  ) -> tuple[bool, str]:
    """
    Get a file from API
    ---
    Arguments
      - file_id: File ID to get (required)
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
    self,
    commands: list[TelegramCommand],
    scope: TelegramCommandsScope = TelegramCommandsScope.ALL,
    language: str = None,
  ) -> tuple[bool, str | int]:
    """
    Set the commands list for the bot
    ---
    Arguments
      - commands: List of commands (required)
      - scope: Scope of the commands (optional)
      - language: Locale or Language locale of the commands list (optional)
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
    self,
    scope: TelegramCommandsScope = TelegramCommandsScope.ALL,
    language: str = None,
  ) -> tuple[bool, str | int]:
    """
    Delete current commands
    ---
    Arguments
      - scope: Scope of the commands (optional)
      - language: Locale or Language locale of the commands list (optional)
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
    self,
    chat_id: str | int,
  ) -> bool:
    """
    Leave Chat
    ---
    Arguments
      - chat_id: Chat ID that will exit (required)
    """
    if not isinstance(chat_id, (str, int)):
      raise TelegramException(exception=f'chat_id must be str or int, received {type(chat_id)}')

    log.debug('Leaving chat %s', chat_id)
    with requests.post(f'{self.base_url}/leaveChat', {'chat_id': chat_id}) as req:
      response = req.json()

    return response['ok']

  def set_webhook(self, uri: str) -> bool:
    """
    Set Webhook
    ---
    Arguments
      - uri: URI to set as webhook (required)
    """
    if not isinstance(uri, str):
      raise TelegramException(exception=f'uri must be str, received {type(uri)}')

    payload = {'url': uri, 'allowed_updates': ['message', 'edited_message'], 'drop_pending_updates': True}

    log.debug('Setting webhook: %s', payload)
    with requests.post(f'{self.base_url}/setWebhook', payload) as req:
      response = req.json()

    return response['ok']

  def delete_webhook(self) -> bool:
    """
    Delete Webhook
    """

    log.debug('Deleting webhook')
    with requests.post(f'{self.base_url}/deleteWebhook') as req:
      response = req.json()

    return response['ok']
