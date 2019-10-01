# -*- coding: utf-8 -*-

import argparse
import webbrowser
import logging
import os

import tornado.ioloop
import tornado.web

import views.chat
import views.config
import views.main

logger = logging.getLogger(__name__)

WEB_ROOT = os.path.join(os.path.dirname(__file__), 'frontend', 'dist')


def main():
    parser = argparse.ArgumentParser(description='用于OBS的仿YouTube风格的bilibili直播聊天层')
    parser.add_argument('--host', help='服务器host，默认为127.0.0.1', default='127.0.0.1')
    parser.add_argument('--port', help='服务器端口，默认为12450', type=int, default=12450)
    parser.add_argument('--debug', help='调试模式', action='store_true')
    args = parser.parse_args()

    logging.basicConfig(
        format='{asctime} {levelname} [{name}]: {message}',
        datefmt='%Y-%m-%d %H:%M:%S',
        style='{',
        level=logging.INFO if not args.debug else logging.DEBUG
    )

    app = tornado.web.Application(
        [
            (r'/chat', views.chat.ChatHandler),
            (r'/config', views.config.ConfigsHandler),
            (r'/config/(.+)', views.config.ConfigHandler),

            (r'/((css|fonts|img|js|static)/.*)', tornado.web.StaticFileHandler, {'path': WEB_ROOT}),
            (r'/(favicon\.ico)', tornado.web.StaticFileHandler, {'path': WEB_ROOT}),
            (r'/.*', views.main.MainHandler, {'path': WEB_ROOT})
        ],
        websocket_ping_interval=30,
        debug=args.debug,
        autoreload=False
    )
    app.listen(args.port, args.host)
    logger.info('Server started: %s:%d', args.host, args.port)
    url = 'http://localhost' if args.port == 80 else f'http://localhost:{args.port}'
    webbrowser.open(url)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
