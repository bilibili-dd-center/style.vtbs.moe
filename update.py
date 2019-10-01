# -*- coding: utf-8 -*-

import aiohttp

VERSION = 'v1.1.4'


async def check_update():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.github.com/repos/xfgryujk/blivechat/releases/latest') as r:
            data = await r.json()
            if data['name'] != VERSION:
                print('New version available:', data['name'])
                print(data['body'])
                print('Download:', data['html_url'])
