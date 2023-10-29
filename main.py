#!/usr/bin/env python3.9

import asyncio
import sys

from lib.application import Application

argv = sys.argv[1:]

def main(async_loop, argv):
    app = Application(async_loop, argv)
    app.run()


if __name__ == '__main__':
    async_loop = asyncio.get_event_loop()
    main(async_loop, argv)
