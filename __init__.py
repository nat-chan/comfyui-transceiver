import re
import torch
from transceiver.core import transceiver
from abc import ABCMeta

"""
この__init__.pyファイルはComfyUI/custom_nodesに置かれたときに
ComfyUI/main.pyから動的に探索され、読み込まれる
"""

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

def format_class_name(class_name: str) -> str:
    """先頭以外の大文字の前に空白を挟む"""
    formatted_name = re.sub(r'(?<!^)(?=[A-Z])', ' ', class_name)
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
        new_class = super().__new__(cls, name, bases, attrs|{
            "FUNCTION": "run",
            "CATEGORY": "Transceiver📡",
            "INPUT_TYPES": _,
        })
        NODE_CLASS_MAPPINGS[name] = new_class
        NODE_DISPLAY_NAME_MAPPINGS[name] = format_class_name(name)+"📡"
        return new_class

class SaveImageTransceiver(metaclass=CustomNodeMeta):
    OUTPUT_NODE = True
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("channel",)
    REQUIRED = {
        "channel": ("STRING", {"multiline": False, "default": "channel"}),
        "image": ("IMAGE",),
    }
    def run(
        self,
        channel: str,
        image: torch.Tensor,
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
    }
    def run(
        self,
        channel: str,
    ) -> tuple[str, torch.Tensor]:
        shared_array = transceiver.read_numpy(channel)
        tensor_image = torch.tensor(shared_array)
        return (channel, tensor_image)

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
