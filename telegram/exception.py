""" Exceptions """


class TelegramException(BaseException):
  """ Telegram Exceptions """

  def __init__(self, exception: str):
    """ Initializer or Constructor """
    self._exception = exception

  @property
  def _readable(self) -> str:
    """ Readable property """
    return f"TelegramException: {self._exception}"

  def __str__(self) -> str:
    """ Readable property """
    return self._readable

  def __repr__(self) -> str:
    """ Readable property """
    return self._readable
