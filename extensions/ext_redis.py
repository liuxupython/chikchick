import redis
from redis.connection import Connection


class RedisClientWrapper(redis.Redis):

    def __init__(self):
        self._client = None

    def initialize(self, client):
        if self._client is None:
            self._client = client

    def __getattr__(self, item):
        if self._client is None:
            raise RuntimeError("Redis client is not initialized. Call init_app first.")
        return getattr(self._client, item)


redis_client = RedisClientWrapper()


def init_app(app):
    global redis_client
    connection_class = Connection

    redis_params = {
        "username": app.config.get("REDIS_USERNAME"),
        "password": app.config.get("REDIS_PASSWORD"),
        "db": app.config.get("REDIS_DB"),
        "encoding": "utf-8",
        "encoding_errors": "strict",
        "decode_responses": False,
    }

    redis_params.update(
        {
            "host": app.config.get("REDIS_HOST"),
            "port": app.config.get("REDIS_PORT"),
            "connection_class": connection_class,
        }
    )
    pool = redis.ConnectionPool(**redis_params)
    redis_client.initialize(redis.Redis(connection_pool=pool))

    app.extensions["redis"] = redis_client
