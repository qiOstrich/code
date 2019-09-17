import logging
import uuid
import datetime
from base64 import urlsafe_b64encode as b64encode
from base64 import urlsafe_b64decode as b64decode

import tornado.escape
import tornado.websocket

from logics import MsgHistory


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("home.html")

    def post(self):
        username = self.get_argument('username').strip()
        if not username:
            self.redirect('/')
        b64_username = b64encode(username.encode('utf8'))
        self.set_cookie('username', b64_username)
        self.render(
            "chat.html",
            messages=ChatSocketHandler.history.all(),
            clients=ChatSocketHandler.members,
            username=username
        )


class ChatSocketHandler(tornado.websocket.WebSocketHandler):
    members = set()
    history = MsgHistory()
    client_id = 0

    def get_compression_options(self):
        # Non-None enables compression with default options.
        return {}

    def open(self):
        ChatSocketHandler.client_id += 1
        self.client_id = ChatSocketHandler.client_id
        b64_name = self.get_cookie('username')
        if not b64_name:
            self.username = "游客%d" % self.client_id
        else:
            self.username = b64decode(b64_name).decode('utf8')
        ChatSocketHandler.members.add(self)

        message = {
            "id": str(uuid.uuid4()),
            "type": "online",
            "client_id": self.client_id,
            "username": self.username,
            "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        ChatSocketHandler.broadcast(message)

    def on_close(self):
        ChatSocketHandler.members.remove(self)
        message = {
            "id": str(uuid.uuid4()),
            "type": "offline",
            "client_id": self.client_id,
            "username": self.username,
            "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        ChatSocketHandler.broadcast(message)

    @classmethod
    def broadcast(cls, message):
        logging.info("sending message to %d members", len(cls.members))
        for member in cls.members:
            try:
                member.write_message(message)
            except:
                logging.error("Error sending message", exc_info=True)

    def on_message(self, message):
        logging.info("got message %r", message)
        parsed = tornado.escape.json_decode(message)
        self.username = parsed["username"]
        message = {
            "id": str(uuid.uuid4()),
            "body": parsed["body"],
            "type": "message",
            "client_id": self.client_id,
            "username": self.username,
            "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        message["html"] = tornado.escape.to_basestring(
            self.render_string("message.html", message=message)
        )

        ChatSocketHandler.history.add(message)
        ChatSocketHandler.broadcast(message)
