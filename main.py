#!/usr/bin/env python3.9

import asyncio


def main(async_loop):
    app = Application(async_loop)
    app.run()


if __name__ == '__main__':
    async_loop = asyncio.get_event_loop()
    main(async_loop)
