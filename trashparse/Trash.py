from __future__ import unicode_literals
from . _helper import bytes_to_long, long_to_bytes
from . _util import UTCTime

import os


try:
    import builtins
except ImportError:
    import __builtin__

    builtins = __builtin__


class Trash(object):
    def __init__(self, path):
        self.handle = open(path, 'rb')
        self.rawdata = self.handle.read()

    @property
    def info(self):
        if self.filename.startswith('$I'):
            return TrashInfo(self.rawdata)

        return TrashInfo2(self.rawdata)

    @property
    def name(self):
        return self.handle.name

    @property
    def dirname(self):
        return os.path.dirname(self.name)

    @property
    def filename(self):
        return os.path.basename(self.name)

    @property
    def type(self):
        if self.filename.startswith('$I'):
            return '$I'

        return 'INFO2'

    @property
    def content(self):
        path = os.path.join(
            self.dirname, '$R'
          + self.filename[2:]
        )

        with open(path) as handle:
            return handle.read()
            

class TrashInfo(object):
    def __init__(self, data):
        self.data = data

    @property
    def version(self):
        if bytes_to_long(self.data[:4]) == 2:
            return 'Windows 10'
        
        return 'Windows Vista/8/8.1'

    @property
    def filesize(self):
        return bytes_to_long(self.data[8:16])

    @property
    def deleted_time(self):
        return bytes_to_long(self.data[16:24])

    @property
    def path_length(self):
        if self.version == 'Windows 10':
            return bytes_to_long(self.data[24:28])

    @property
    def path(self):
        if self.version == 'Windows 10':
            pathname = self.data[28:]
        else:
            pathname = self.data[24:]

        try:
            pathname = pathname[::2][:-1].decode()
        except UnicodeError:
            pathname = pathname[::2][:-1].decode('ISO-8859-1')

        return pathname.strip('\x00')


class TrashInfo2(Trash):
    pass


def inspect(path):
    basename = os.path.basename(path)

    assert (
        basename.startswith('$I') or
        basename.startswith('INFO2')
    )

    return Trash(path)