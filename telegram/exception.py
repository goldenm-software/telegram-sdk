"""Exceptions"""

import sys

if sys.version_info >= (3, 11):
  from typing import Self
else:
  from typing_extensions import Self


class TelegramException(BaseException):
  """Telegram Exceptions"""

  def __init__(self: Self, exception: str) -> None:
    """
    Telegram Exception

    :param exception: Exception message
    :type exception: str
    """
    self._exception = exception

  @property
  def _readable(self: Self) -> str:
    """Readable property"""
    return f'TelegramException: {self._exception}'

  def __str__(self: Self) -> str:
    """Readable property"""
    return self._readable

  def __repr__(self: Self) -> str:
    """Readable property"""
    return self._readable


__all__ = ['TelegramException']
