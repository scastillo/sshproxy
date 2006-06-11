#!/usr/bin/env python
# -*- coding: ISO-8859-15 -*-
#
# Copyright (C) 2005-2006 David Guerizec <david@guerizec.net>
#
# Last modified: 2006 Jun 11, 02:41:38 by david
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA

from config import get_config

class PasswordDatabase(object):
    backend_id = ''
    backends = {}
    backend = None

    @classmethod
    def register_backend(cls):
        if not cls.backend_id:
            raise AttributeError('Backend error:'
                    ' missing attribute backend_id for %s', cls)
        if not cls.backends.has_key(cls.backend_id):
            cls.backends[cls.backend_id] = cls
        print "REGISTERING", str(cls)

    def __call__(self):
        if self.backend is None:
            backend = get_config('sshproxy')['pwdb_backend']

            self.backend = self.backends[backend]()
        return self.backend

    def get_console(self):
        return None

get_backend = PasswordDatabase()


class UserEntry(object):
    def __init__(self, uid, password, primary=0):
        self.uid = uid
        self.password = password
        self.primary = primary

    def __repr__(self):
        return str({'uid': self.uid,
                    'password': '*'*len(self.password),
                    'primary': self.primary})

class SiteEntry(object):
    def __init__(self, sid, ip_address=None, port=22, location=None,
                       user_list=None):
        self.sid = sid
        self.ip_address = ip_address
        self.port = port
        self.location = location
        
        self.users = {}
        
        if user_list is None:
            return
        for user in user_list:
            self.users[user.uid] = user

    def default_user(self):
        for u in self.users.keys():
            if self.users[u].primary:
                return u
        return None

    def get_user(self, uid):
        if self.users.has_key(uid):
            return self.users[uid]
        else:
            return None

    def __repr__(self):
        return 'SiteEntry: %s %s:%s (%s) %s' % (self.sid,
                                                self.ip_address,
                                                self.port,
                                                self.location,
                                                repr(self.users))

class FileBackend(PasswordDatabase):
    backend_id = 'file'

    def __init__(self, site_list=None):
        self.sites = {}
        self.login = None

        if site_list is None:
            return
        for site in site_list:
            self.sites[site.sid] = site

    def get_console(self):
        return None

    def get_user_site(self, sid):
        user = None
        if sid.find('@') >= 0:
            user, sid = sid.split('@')
        if self.sites.has_key(sid):
            if user and self.sites[sid].get_user(user):
                return user, self.sites[sid]
            elif not user and self.sites[sid].default_user():
                return self.sites[sid].default_user(), self.sites[sid]
                
        return None, None

    def list_sites(self):
        return self.sites.keys()

    def is_admin(self, user=None):
        return True

    def is_allowed(self, username, password=None, key=None):
        return True

    def can_connect(self, user, site):
        return True

FileBackend.register_backend()