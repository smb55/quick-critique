from typing import List, Optional
from __future__ import absolute_import, unicode_literals
from .celery import app as celery_app

__all__ = ("celery_app",)

TRUE = ("1", "true", "True", "TRUE", "on", "yes")


def is_true(val: Optional[str]) -> bool:
    return val in TRUE


def split_with_comma(val: str) -> List[str]:
    return list(filter(None, map(str.strip, val.split(","))))
