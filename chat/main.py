#!/usr/bin/env python

import os
import logging

import tornado.web
import tornado.ioloop
from tornado.options import define, options, parse_command_line

from views import MainHandler, ChatSocketHandler

define("host", default='0.0.0.0', help="地址", type=str)
define("port", default=8000, help="端口", type=int)


def main():
    parse_command_line()

    web_app = tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/chatsocket", ChatSocketHandler),
        ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "statics"),
    )
    web_app.listen(options.port, options.host)

    logging.info('Server running on %s:%s' % (options.host, options.port))
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
