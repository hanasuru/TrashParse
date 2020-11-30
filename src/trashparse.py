#!/usr/bin/python2

from argparse import ArgumentParser
from collections import OrderedDict
from datetime import datetime, timedelta, tzinfo
from calendar import timegm

import os
import glob
import struct
import logging

EPOCH_AS_FILETIME = 116444736000000000  # January 1, 1970 as MS file time
HUNDREDS_OF_NANOSECONDS = 10000000
HOUR = timedelta(hours=1)


class UTC(tzinfo):
    def utcoffset(self, dt):
        return timedelta(0)

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return timedelta(0)

class WinTime(object):
    @staticmethod
    def time_to_date(ft):
        return datetime.utcfromtimestamp((ft - EPOCH_AS_FILETIME) / HUNDREDS_OF_NANOSECONDS)

    @staticmethod
    def date_to_time(dt):
        if (dt.tzinfo is None) or (dt.tzinfo.utcoffset(dt) is None):
            dt = dt.replace(tzinfo=utc)
    
        return EPOCH_AS_FILETIME + (timegm(dt.timetuple()) * HUNDREDS_OF_NANOSECONDS)


class Info(object):
    def __init__(self, content):
        self.content = content
        self.version = self.get_version()
        self.filesize = self.get_file_size()
        self.timestamp = self.get_deleted_time()
        self.namelen = self.get_filename_length()
        self.filename = self.get_filename()

    def get_version(self):
        if self.content[0] == '\x02':
            return 'Windows 10'
        return 'Windows 8'        

    def get_file_size(self):
        return struct.unpack('<Q', self.content[8:16])[0]

    def get_deleted_time(self):
        return struct.unpack('<Q', self.content[16:24])[0]

    def get_filename_length(self):
        if self.version == 'Windows 10':
            return struct.unpack('<I', self.content[24:28])[0]

    def get_filename(self):
        path = self.content[24:]
        if self.version == 'Windows 10':
            path = self.content[28:]

        return path[::2].strip('\x00')


class IRParser(object):
    def __init__(self, icontent, rcontent):
        self.icontent = icontent
        self.rcontent = rcontent

    @property
    def info(self):
        return Info(self.icontent)

    @property
    def content(self):
        return self.rcontent


class TrashParse(object):
    def __init__(self, directory):
        self.directory = directory
        self.identifier = {}
        self.result = OrderedDict()
        self.utc = UTC()
    
    def recurse(self):
        files = glob.glob('{}/*[!\.ini]'.format(self.directory))

        for file in files:
            id = file.split('/')[-1][2:]
            count = self.identifier.get(id, 0)
            count += 1

            self.identifier[id] = count

    def parse(self):
        basedir = self.directory

        for id, count in self.identifier.iteritems():
            if count != 2:
                logging.error('{} can\'t be processed'.format(id))
                logging.error('Reason: Either $I or $R is missing\n')
            else:
                icontent = open('{}/$I{}'.format(basedir, id), 'rb').read()
                rcontent = open('{}/$R{}'.format(basedir, id), 'rb').read()
                parsed = IRParser(icontent, rcontent)

                self.result[id] = parsed

    def sort_by(self, filter=None):

        if filter == 'size':
            temp = sorted(
                self.result.items(), key=lambda x: x[1].info.filesize
            )
        elif filter == 'time':
            temp = sorted(
                self.result.items(), key=lambda x: x[1].info.timestamp
            )
        elif filter == 'name':
            temp = sorted(
                self.result.items(), key=lambda x: x[1].info.filename
            )            

        self.result = OrderedDict(temp)
        return self

    def display(self, quiet=False):
        columns = ['Id', 'Size', 'Original Path', 'Version', 'Deleted Time (UTC)']
        template = '{0:<12}{1:<8}{2:<40}{3:<15}{4:}'
        content = template.format(*columns)

        if not quiet: print(content)

        for id, items in self.result.iteritems():
            info = items.info

            rows = template.format(
                id, info.filesize,
                info.filename, info.version,
                WinTime.time_to_date(info.timestamp)
            )

            if not quiet: print(rows)
            content += '\n{}'.format(rows)

        if quiet:
            with open('reports.txt', 'wb') as file:
                file.write(content)

    def extract(self):
        try:
            os.makedirs('files')
        except OSError:
            pass

        filled = {}
        for items in self.result.values():
            info = items.info
            filename = info.filename.split('\\')[-1]
            
            count = filled.get(filename, 0)
            count += 1
            filled[filename] = count

            if count != 1:
                numbering = '({}).'.format(count)
                filename = numbering.join(filename.split('.'))
            
            pathname = os.path.join('files', filename)
            with open(pathname, 'wb') as f:
                f.write(items.content)           

if __name__ == "__main__":
    parser = ArgumentParser(description='Simple Recycle.Bin Windows Parser')
    parser.add_argument('path', metavar='directory', help='target directory')
    parser.add_argument('--sort', '-s', metavar='attribute', default=None, help='Sort by attribute (name, time, size)')
    parser.add_argument('--extract', '-e', action='store_true', help='Extract & dump bin into files')
    parser.add_argument('--quiet', '-q', action='store_true', help='quiet (Don\'t show list file)')
    arguments = parser.parse_args()

    tbin = TrashParse(arguments.path)
    tbin.recurse()
    tbin.parse()
    
    if arguments.sort:
        tbin.sort_by(arguments.sort)
    if arguments.extract:
        tbin.extract()
    
    tbin.display(arguments.quiet)