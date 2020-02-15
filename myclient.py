#!/usr/local/opt/python/bin/python3.7
# -*- coding: utf-8 -*-
import _thread
import re
import sys

import shadowsocks.local
import shadowsocks.server


if __name__ == '__main__':
    sys.argv = ['sslocal', '-c', 'ss-config.json']
    shadowsocks.local.main()
