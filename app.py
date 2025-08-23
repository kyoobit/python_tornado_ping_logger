import asyncio
import logging
import json

from datetime import datetime
from pathlib import Path

# python -m pip show tornado
# python -m pip install --upgrade pip tornado
import tornado.web
from tornado.log import access_log


def log_function(handler, *args, **kwargs):
    """Writes a completed HTTP request to the `access_log'

    See Also:
        https://www.tornadoweb.org/en/stable/web.html#application-configuration
    """
    if handler.get_status() == 404 or handler.get_status() < 400:
        _log_method = access_log.info
    elif handler.get_status() < 500:
        _log_method = access_log.warning
    else:
        _log_method = access_log.error
    request_time = 1000.0 * handler.request.request_time()
    _log_method(
        "{status} {method} {full_url} {duration:0.2f}ms {forwarded}".format(
            status=handler.get_status(),
            method=handler.request.method,
            full_url=handler.request.full_url(),
            duration=request_time,
            forwarded=handler.request.headers.get("forwarded", "-"),
        )
    )


class DefaultHandler(tornado.web.RequestHandler):

    def initialize(self, **kwargs):
        name = f"{Path(__file__).name} -"
        logging.debug(f"{name} initialize - **kwargs: {kwargs!r}")
        self.set_header("Server", "Python/Tornado/Ping")

    def get(self, *args, **kwargs):
        name = f"{Path(__file__).name} -"
        logging.debug(f"{name} get - *args: {args!r}")
        logging.debug(f"{name} get - **kwargs: {kwargs!r}")

        # Always return 204
        self.set_status(204)


class PingHandler(tornado.web.RequestHandler):

    def initialize(self, **kwargs):
        name = f"{Path(__file__).name} -"
        logging.debug(f"{name} initialize - **kwargs: {kwargs!r}")
        self.set_header("Server", "Python/Tornado/Ping")

    def get(self, *args, **kwargs):
        name = f"{Path(__file__).name} -"
        logging.debug(f"{name} get - *args: {args!r}")
        logging.debug(f"{name} get - **kwargs: {kwargs!r}")

        # Always return 200 Pong!
        self.write(f"{self.settings.get('message', 'Pong!')}\n")

    def post(self, *args, **kwargs):
        name = f"{Path(__file__).name} -"
        logging.debug(f"{name} post - *args: {args!r}")
        logging.debug(f"{name} post - **kwargs: {kwargs!r}")

        # Serialize the ping data found in the request body
        serialized_ping = self.serialize_ping_data()

        # Write the serialized request data to standard out
        logging.info(f"PING - {serialized_ping}")

        # Always return 204
        self.set_status(204)

    def serialize_ping_data(self, *args, **kwargs) -> dict:
        """Serialize the ping data into a JSON encoded string"""
        name = f"{Path(__file__).name} -"
        logging.debug(f"{name} serialize_ping_data - *args: {args!r}")
        logging.debug(f"{name} serialize_ping_data - **kwargs: {kwargs!r}")

        # Serialize the request data
        serialized_ping = {
            "timestamp": datetime.now().isoformat(),
            "ping": None,
            "err": None,
        }

        # self.request ---> tornado.httputil.HTTPServerRequest
        # https://www.tornadoweb.org/en/stable/httputil.html#tornado.httputil.HTTPServerRequest
        if self.request.body:
            # Request body data "should be" in JSON format
            try:
                ping = self.request.body.decode()
                serialized_ping.update(ping=json.loads(ping))
            except Exception as err:
                logging.warning(
                    f"Failed JSON load of body data: {self.request.body!r}, exception: '{err}'"
                )
                serialized_ping.update(ping=str(self.request.body))
                serialized_ping.update(err=str(err))

        # Return the serialized ping data
        serialized_ping = json.dumps(serialized_ping)
        return serialized_ping


def make_app(*args, **kwargs):
    return tornado.web.Application(
        [
            (r"/ping", PingHandler),
            (r"/.*", DefaultHandler),
        ],
        debug=kwargs.get("debug", False),
        log_function=log_function,
    )


async def main(*args, **kwargs):
    name = f"{Path(__file__).name} - "
    logging.debug(f"{name} main - *args: {args}")
    logging.debug(f"{name} main - **kwargs: {kwargs}")

    app = make_app(**kwargs)
    app.listen(int(kwargs.get("port", 8888)))
    await asyncio.Event().wait()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
