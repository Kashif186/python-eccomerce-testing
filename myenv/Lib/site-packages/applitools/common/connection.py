import atexit
import logging
import weakref
from json import dumps, loads
from threading import Thread
from time import time
from typing import TYPE_CHECKING

from six import moves
from websocket import WebSocket

from applitools.core_universal import get_instance

from .object_registry import RefId

if TYPE_CHECKING:
    from typing import Optional, Text

    from ..selenium.command_context import CommandContext

_all_sockets = []
_logger = logging.getLogger(__name__)

try:
    from builtins import TimeoutError
except ImportError:

    class TimeoutError(Exception):
        pass


class USDKConnection(object):
    def __init__(self, websocket):
        # type: (WebSocket) -> None
        self._websocket = websocket
        self._response_queues = {}
        weak_socket = weakref.ref(self._websocket)
        self._receiver_thread = Thread(
            target=self._receiver_loop,
            name="USDK Receiver",
            args=(weak_socket, self._response_queues),
        )
        # Receiver threads are designed to exit even if they serve leaked unclosed
        # connections. But non-daemon threads are joined on shutdown deadlocking with
        # garbage collector and atexit manager that should close the socket
        self._receiver_thread.daemon = True
        _all_sockets.append(weak_socket)
        self._receiver_thread.start()

    @classmethod
    def create(cls, server=None):
        # type: (Optional[server.SDKServer]) -> USDKConnection
        server = server or get_instance()
        websocket = WebSocket()
        websocket.connect("ws://localhost:{}/eyes".format(server.port))
        return cls(websocket)

    def notification(self, name, payload):
        # type: (Text, dict) -> None
        self._websocket.send(dumps({"name": name, "payload": payload}))

    def command(self, context, name, payload, wait_timeout):
        # type: (CommandContext, Text, dict, float) -> Optional[dict]
        assert context.key.object_registry_id not in self._response_queues
        queue = moves.queue.Queue()
        self._response_queues[context.key.object_registry_id] = queue
        self._websocket.send(
            dumps({"name": name, "key": str(context.key), "payload": payload})
        )
        deadline = time() + wait_timeout
        while True:
            try:
                event, obj = queue.get(timeout=deadline - time())
            except moves.queue.Empty:
                raise TimeoutError("USDK Command timeout")
            if event == "result":
                return obj
            elif event == "callback":
                context.execute_callback(obj)
            else:
                raise RuntimeError("Unexpected", event, obj)

    def response(self, key, name, result=None, error=None):
        # type: (Text, Text, Optional[dict], Optional[dict]) -> None
        payload = {}
        if result is not None:
            payload["result"] = result
        elif error is not None:
            payload["error"] = error
        data = {"key": key, "name": name, "payload": payload}
        self._websocket.send(dumps(data))

    def close(self):
        if self._websocket:
            self._websocket.close()
            self._websocket = None
            self._receiver_thread = None

    def __del__(self):
        self.close()

    @staticmethod
    def _receiver_loop(weak_socket, response_queues):
        while True:
            try:
                socket = weak_socket()
                if not socket:
                    raise EOFError
                response = socket.recv()
                del socket
                if not response:
                    raise EOFError
                response = loads(response)
                command_name = response["name"]
                if command_name.startswith("Driver."):  # specdriver callback
                    key = command_key(response)
                    response_queues[key.object_registry_id].put(("callback", response))
                elif command_name == "Logger.log":
                    entry = response["payload"]
                    level = logging.getLevelName(entry["level"].upper())
                    _logger.log(level, entry["message"])
                else:
                    key = RefId.from_str(response["key"])
                    response_queues.pop(key.object_registry_id).put(
                        ("result", response)
                    )
            except Exception as exc:
                socket = weak_socket()
                if socket:
                    socket.abort()
                for queue in response_queues.values():
                    queue.put(("exception", exc))
                break


def command_key(response):
    # type: (dict) -> RefId
    payload = response["payload"]
    if "context" in payload:
        obj_id = payload["context"]["applitools-ref-id"]
    else:
        obj_id = payload["driver"]["applitools-ref-id"]
    return RefId.from_str(obj_id)


@atexit.register
def ensure_all_closed():
    for weak_ref in _all_sockets:
        socket = weak_ref()
        if socket:
            socket.close()
