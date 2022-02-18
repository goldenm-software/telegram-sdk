""" Exceptions """

class TelegramException(BaseException):
  """ Telegram Exceptions """
  def __init__(self, exception):
    """ Initializer or Constructor """
    self.__exception = exception

  @property
  def __readable(self):
    """ Readable property """
    return f"TelegramException({self.__exception})"

  def __str__(self):
    """ Readable property """
    return self.__readable

  def __repr__(self):
    """ Readable property """
    return self.__readable
