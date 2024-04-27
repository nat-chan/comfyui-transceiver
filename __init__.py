import torch
from transceiver.core import transceiver

"""
この__init__.pyファイルはComfyUI/custom_nodesに置かれたときに
ComfyUI/main.pyから動的に探索され、読み込まれる
"""

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}
class CustomNodeMeta(type):
    def __new__(
        cls,
        name: str,
        bases: list,
        attrs: dict,
    ) -> "CustomNodeMeta":
        global NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS
        new_class = super().__new__(cls, name, bases, attrs|{"FUNCTION": "run", "CATEGORY": "Transceiver📡"})
        NODE_CLASS_MAPPINGS[name] = new_class
        NODE_DISPLAY_NAME_MAPPINGS[name] = name
        return new_class

class SaveImageTransceiver(metaclass=CustomNodeMeta):
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("channel",)
    OUTPUT_NODE = True
    @classmethod
    def INPUT_TYPES(self):
        return {
            "required": {
                "channel": ("STRING", {"multiline": False, "default": "channel"}),
                "image": ("IMAGE",),
            },
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
    RETURN_TYPES = ("STRING", "IMAGE")
    RETURN_NAMES = ("channel", "image")
    OUTPUT_NODE = True
    @classmethod
    def INPUT_TYPES(self):
        return {
            "required": {
                "channel": ("STRING", {"multiline": False, "default": "channel"}),
            },
        }
    def run(
        self,
        channel: str,
    ) -> tuple[str, torch.Tensor]:
        shared_array = transceiver.read_numpy(channel)
        tensor_image = torch.tensor(shared_array)
        return (channel, tensor_image)

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
