#!/usr/bin/python
# -*- coding: ISO-8859-15 -*-
#
# Copyright (C) 2005 David Guerizec <david@guerizec.net>
#
# Last modified: 2006 jan 20, 11:49:35 by david
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307  USA


# Imports from Python
import os, sys, logging, logging.handlers
#from paramiko.util import get_thread_id

__all__ = [ 'debug', 'info', 'warning', 'error', 'critical', 'exception' ]

clientLogger = logging.getLogger('sshproxy.client')
clientLogger.setLevel(logging.DEBUG)
socketHandler = logging.handlers.SocketHandler('localhost',
                    logging.handlers.DEFAULT_TCP_LOGGING_PORT)
clientLogger.addHandler(socketHandler)

class PFilter (object):
    def filter(self, record):
#        record._threadid = get_thread_id()
        record._pid = os.getpid()
        return True
_pfilter = PFilter()

def get_logger(name):
    l = logging.getLogger(name)
    l.addFilter(_pfilter)
    return l

# the following for loop does the same thing as the
# following line for all __all__ elements
# info = get_logger('sshproxy.client').info
self = sys.modules[__name__]
logger = get_logger('sshproxy.client')
for func in __all__:
    setattr(self, func, getattr(logger, func))


