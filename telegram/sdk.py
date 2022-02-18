""" Telegram SDK """
import logging
import json
from datetime import datetime
import requests
from .exception import TelegramException
from .helpers import TelegramModes, TelegramKeyboard, TelegramCommandsScope, TelegramCommand

class TelegramSdk:
  """ Telegram bot sdk """
  def __init__(self, token, host='https://api.telegram.org'):
    """ constructor """
    self.__log = logging.getLogger('telegram.sdk')
    self.token = token
    self.host = host

  @property
  def base_url(self):
    """ Base URL """
    return f'{self.host}/bot{self.token}'

  def send_sticker(self, chat_id, sticker, silent=False):
    """ Send sticker """
    if not isinstance(sticker, str):
      raise TelegramException(exception=f'sticker should be str, received {type(sticker)}')
    if not isinstance(chat_id, (str, int)):
      raise TelegramException(exception=f'chat_id must be str or int, received {type(chat_id)}')
    if not isinstance(silent, bool):
      raise TelegramException(exception=f'silent must be bool, received {type(silent)}')

    payload = {
      'chat_id': chat_id,
      'sticker': sticker,
      'disable_notification': silent
    }
    with requests.post(f'{self.base_url}/sendSticker', payload) as req:
      response = req.json()

    if 'description' in response:
      return response['ok'], response['description']
    return response['ok'], response['result']['message_id']

  def send_message(self, chat_id, message, mode=TelegramModes.HTML, silent=False, reply_id=None, disable_preview=False, keyboard=TelegramKeyboard()):
    """
      Send a message

      Arguments
      ---------
        chat_id   (str, int)        required    Chat ID to send the message
        message   str               required    Message to send, maximum length allowed: 1-4096 characters
        mode      TelegramModes     optional    Message operation mode
        silent    bool              optional    Indicates if the message will emit a sound or not when received
        reply_id  (str, int)        optional    Message ID to reply
        keyboard  TelegramKeyboard  optional    An instance of TelegramKeyboard with choices, empty by default.
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

    with requests.post(f'{self.base_url}/sendMessage', payload) as req:
      response = req.json()

    if 'description' in response:
      return response['ok'], response['description']
    return response['ok'], response['result']['message_id']

  def send_image(self, chat_id, image_uri, caption=None):
    """
    Send image
    
    Arguments
    ---------
      chat_id       (str, int)        required    Chat ID to send the message
      image_uri     str               required    Image URI
    """
    if not isinstance(chat_id, (str, int)):
      raise TelegramException(exception=f'chat_id must be str or int, received {type(chat_id)}')

    if caption is not None:
      if not isinstance(caption, (str, int)):
        raise TelegramException(exception=f'caption must be str or int, received {type(caption)}')
      if len(caption) < 1:
        raise TelegramException(exception=f'caption should be greater than or equals to 1, received {len(message)}')
      if len(caption) > 1024:
        raise TelegramException(exception=f'caption should be less than or equals to 1024, received {len(message)}')

    payload = {
      'chat_id': chat_id,
      'photo': image_uri
    }

    if caption is not None:
      payload['caption'] = caption

    with requests.post(f'{self.base_url}/sendPhoto', payload) as req:
      response = req.json()

    if 'description' in response:
      return response['ok'], response['description']
    return response['ok'], response['result']['message_id']


  def send_poll(self, chat_id, question, options, anonymous=False, silent=False, multiple=False, close_date=None):
    """
    Send poll
    
    Arguments
      ---------
        chat_id       (str, int)        required    Chat ID to send the message
        question      str               required    Question to send, maximum length allowed: 1-300 characters
        options       list(str)         required    Choices to select
        anonymous     bool              optional    Indicates if the poll could be submitted as Anonymous.
        silent        bool              optional    Silent notification
        multiple      bool              optional    Allow to submit multiple choices.
        close_date    int               optional    Set the expiration date of the poll (In Unix Timestamp)
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
        raise TelegramException(exception=f'option[{i}] must be less than or equals to 100 characters, received {len(option)}')
      
      if len(option) < 1:
        raise TelegramException(exception=f'option[{i}] must be greater than or equals to 1 character, received {len(option)}')

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

    with requests.post(f'{self.base_url}/sendPoll', payload) as req:
      response = req.json()

    if 'description' in response:
      return response['ok'], response['description']
    return response['ok'], response['result']['message_id']

  def stop_poll(self, chat_id, poll_id):
    """
    Stop poll
    
    Arguments
    ---------
      chat_id       (str, int)    required    Chat ID where Poll is submitted
      poll_id       (str, int)    required    Message ID where poll is submitted
    """
    if not isinstance(chat_id, (str, int)):
      raise TelegramException(exception=f'chat_id must be str or int, received {type(chat_id)}')
    if not isinstance(poll_id, (str, int)):
      raise TelegramException(exception=f'poll_id must be str or int, received {type(poll_id)}')

    payload = {
      'chat_id': chat_id,
      'message_id': poll_id
    }

    with requests.post(f'{self.base_url}/stopPoll', payload) as req:
      response = req.json()

    if 'description' in response:
      return response['ok'], response['description']
    return response['ok'], response['result']['id']

  def get_file(self, file_id):
    """
    Get a file from API
    
    Arguments
    ---------
      file_id   str   required    File ID to get
    """

    if not isinstance(file_id, str):
      raise TelegramException(exception=f'file_id should be str, received {type(file_id)}')

    payload = {
      'file_id': file_id
    }

    with requests.post(f'{self.base_url}/getFile', payload) as req:
      response = req.json()

    if 'description' in response:
      return response['ok'], response['description']
    return response['ok'], response['result']['file_path']

  def set_commands(self, commands, scope=TelegramCommandsScope.ALL, language=None):
    """
    Set Commands

    Arguments
    ---------
      commands      list(TelegramCommand)   required    List of commands
      scope         TelegramCommandsScope   optional    Scope of the commands
      language      str                     optional    Locale or Language locale of the commands list
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
        raise TelegramException(exception=f'language must be a 2 character ISO 639-1 code')

    parsed_commands = []

    for command in commands:
      parsed_commands.append(command.telegram)

    payload = {
      'commands': json.dumps(parsed_commands),
      'scope': scope.telegram
    }

    if language is not None:
      payload['language_code'] = language

    with requests.post(f'{self.base_url}/setMyCommands', payload) as req:
      response = req.json()

    if 'description' in response:
      return response['ok'], response['description']
    return response['ok'], response['result']

  def delete_commands(self, scope=TelegramCommandsScope.ALL, language=None):
    """
    Delete current commands

    Arguments
    ---------
      scope         TelegramCommandsScope   optional    Scope of the commands
      language      str                     optional    Locale or Language locale of the commands list
    """
    if not isinstance(scope, TelegramCommandsScope):
      raise TelegramException(exception=f'scope must be TelegramCommandsScope, received {type(scope)}')

    if language is not None:
      if not isinstance(language, str):
        raise TelegramException(exception=f'language must be str, received {type(language)}')

      if len(language) != 2:
        raise TelegramException(exception=f'language must be a 2 character ISO 639-1 code')

    payload = {
      'scope': scope.telegram
    }

    if language is not None:
      payload['language_code'] = language

    with requests.post(f'{self.base_url}/deleteMyCommands', payload) as req:
      response = req.json()

    if 'description' in response:
      return response['ok'], response['description']
    return response['ok'], response['result']

  def leave_chat(self, chat_id):
    """
    Leave Chat
    
    Arguments
    ---------
      chat_id       (str, int)    required    Chat ID that will exit
    """
    if not isinstance(chat_id, (str, int)):
      raise TelegramException(exception=f'chat_id must be str or int, received {type(chat_id)}')

    with requests.post(f'{self.base_url}/leaveChat', {'chat_id': chat_id}) as req:
      response = req.json()

    return response['ok']

  def set_webhook(self, uri):
    """
    Set Webhook
    
    Arguments
    ---------
      uri    str required    Chat ID that will exit
    """
    if not isinstance(uri, str):
      raise TelegramException(exception=f'uri must be str, received {type(uri)}')

    payload = {
      'url': uri,
      'allowed_updates': ['message', 'edited_message'],
      'drop_pending_updates': True
    }

    with requests.post(f'{self.base_url}/setWebhook', payload) as req:
      response = req.json()

    return response['ok']

  def delete_webhook(self):
    """
    Delete Webhook
    """

    with requests.post(f'{self.base_url}/deleteWebhook') as req:
      response = req.json()

    return response['ok']