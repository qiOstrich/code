# ！ /bin/env python
import tornado.ioloop
import tornado.web
from tornado.options import parse_command_line, define, options

'''
通过tornado创建服务器
'''
define("host", default='0.0.0.0', help='主机地址', type=str)
define("port", default=8880, help='主机端口', type=int)

parse_command_line()
print('你传入的host：%s' % options.host)
print('你传入的port：%s' % options.port)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('<h1>你打开了一个好东西</h1>')


class StoryHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('<h2>你并不是对的人</h2>', )


def make_app():
    return tornado.web.Application([
        (r'/', MainHandler),
        (r'/main', MainHandler),
        (r'/story', StoryHandler)
    ])


if __name__ == '__main__':
    app = make_app()
    app.listen(8880)
    tornado.ioloop.IOLoop.current().start()
