# -*- coding: utf-8 -*-

from enum import Enum

class PendingStatus(Enum):
    """
     四种交易状态
    """
    waiting = 1
    success = 2
    reject = 3
    redraw = 4
