import json

from redis import Redis

rds = Redis()


class MsgHistory:
    key = 'chat_history'
    size = 10

    @classmethod
    def add(cls, msg):
        json_msg = json.dumps(msg)
        rds.rpush(cls.key, json_msg)
        rds.ltrim(cls.key, -cls.size, -1)

    @classmethod
    def all(cls):
        all_msg = []
        for json_msg in rds.lrange(cls.key, 0, cls.size-1):
            msg = json.loads(json_msg)
            all_msg.append(msg)
        return all_msg
