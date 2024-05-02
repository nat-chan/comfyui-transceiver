import re
from abc import ABCMeta
from pprint import pprint

import aiohttp
import torch
from aiohttp import web
from server import PromptServer  # noqa
from transceiver.core import transceiver

"""
この__init__.pyファイルはComfyUI/custom_nodesに置かれたときに
ComfyUI/main.pyから動的に探索され、読み込まれる
参考URL:
https://github.com/chrisgoringe/Comfy-Custom-Node-How-To/wiki/api
https://github.com/chrisgoringe/Comfy-Custom-Node-How-To/wiki/data_types
https://zenn.dev/4kk11/articles/4e36fc68293bd2
"""

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}
WEB_DIRECTORY = "./js"
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]


def format_class_name(class_name: str) -> str:
    """先頭以外の大文字の前に空白を挟む"""
    formatted_name = re.sub(r"(?<!^)(?=[A-Z])", " ", class_name)
    return formatted_name


class CustomNodeMeta(ABCMeta):
    def __new__(
        cls,
        name: str,
        bases: list,
        attrs: dict,
    ) -> "CustomNodeMeta":
        global NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

        @classmethod
        def _(cls):
            return {"required": cls.REQUIRED}

        new_class = super().__new__(
            cls,
            name,
            bases,
            attrs
            | {
                "FUNCTION": "run",
                "CATEGORY": "Transceiver📡",
                "INPUT_TYPES": _,
            },
        )
        NODE_CLASS_MAPPINGS[name] = new_class
        NODE_DISPLAY_NAME_MAPPINGS[name] = format_class_name(name) + "📡"
        return new_class


class SaveImageTransceiver(metaclass=CustomNodeMeta):
    OUTPUT_NODE = True
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("channel",)
    REQUIRED = {
        "channel": ("STRING", {"multiline": False, "default": "channel"}),
        "image": ("IMAGE",),
        "seed": ("INT:seed", {}),
    }

    def run(
        self,
        channel: str,
        image: torch.Tensor,
        seed: int,
    ) -> tuple[str]:
        original_array = image.detach().cpu().numpy()
        transceiver.write_numpy(channel, original_array)
        return (channel,)


class LoadImageTransceiver(metaclass=CustomNodeMeta):
    OUTPUT_NODE = True
    RETURN_TYPES = ("STRING", "IMAGE")
    RETURN_NAMES = ("channel", "image")
    REQUIRED = {
        "channel": ("STRING", {"multiline": False, "default": "channel"}),
        "seed": ("INT:seed", {}),
    }

    def run(
        self,
        channel: str,
        seed: int,
    ) -> tuple[str, torch.Tensor]:
        shared_array = transceiver.read_numpy(channel)
        tensor_image = torch.tensor(shared_array)
        return (channel, tensor_image)


# {{{ server ---
routes: aiohttp.web_routedef.RouteTableDef = PromptServer.instance.routes
app: aiohttp.web_app.Application = PromptServer.instance.app


@routes.post("/transceiver_send_to_channel")
async def transceiver_send_to_channel(
    request: aiohttp.web_request.Request,
) -> aiohttp.web_response.Response:
    channel = request.query.get("channel")
    if channel is None:
        return web.Response(status=400, text="channel query parameter is required")
    post = await request.post()
    print("channel:", channel)
    print("post:", post)

    response = web.Response(status=200, text="successfuly sent to channel")
    return response


@routes.get("/transceiver_recieve_from_channel")
async def transceiver_recieve_from_channel(
    request: aiohttp.web_request.Request,
) -> aiohttp.web_response.Response:
    channel = request.query.get("channel")
    if channel is None:
        return web.Response(status=400, text="channel query parameter is required")
    buffer = b"dummy"
    return web.json_response({"buffer": buffer})


async def websocket_handler(request):
    channel = request.query.get("channel")
    action = request.query.get("action")
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    async for message in ws:
        if message.type != aiohttp.WSMsgType.BINARY:
            break
        if action == "send":
            print("channel", channel, type(channel))
            print("action", action, type(action))
            print("message.data", message.data, type(message.data))
            # transceiver.write_numpy(channel, message.data)
        elif action == "recieve":
            # shared_array = transceiver.read_numpy(channel)
            data = b"dummy_data"
            print(channel, action, data)
            await ws.send_bytes(data)
    return ws


app.add_routes([web.get("/transceiver", websocket_handler)])


# --- server }}}
