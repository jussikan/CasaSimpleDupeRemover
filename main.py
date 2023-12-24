#!/usr/bin/env python3.9
# TODO use just 'python3'.

import asyncio
from pathlib import Path
import sys

sys.path.insert(0, Path(__file__).parent)

from lib.application import Application
argv = sys.argv[1:]

def main(async_loop, argv):
    app = Application(async_loop, Path(__file__).parent, argv)
    app.run()


if __name__ == '__main__':
    async_loop = asyncio.get_event_loop()
    main(async_loop, argv)
