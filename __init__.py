import comfy_annotations
import torch
from comfy_annotations import ComfyFunc, ImageTensor, StringInput
from transceiver.core import transceiver

"""
この__init__.pyファイルはComfyUI/custom_nodesに置かれたときに
ComfyUI/main.pyから動的に探索され、読み込まれる
"""

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}


@ComfyFunc(
    category="Transceiver📡",
    display_name="Save Image Transceiver📡",
    is_output_node=True,
    debug=True,
)
def save_image_transceiver(
    image: ImageTensor,
    name: str = StringInput("ComfyUI", multiline=False),
):
    original_array = image.detach().cpu().numpy()
    transceiver.write_numpy(name, original_array)


@ComfyFunc(
    category="Transceiver📡",
    display_name="Load Image Transceiver📡",
    is_output_node=True,
    debug=True,
)
def load_image_transceiver(
    name: str = StringInput("ComfyUI", multiline=False),
) -> ImageTensor:
    shared_array = transceiver.read_numpy(name)
    tensor_image = torch.tensor(shared_array)
    return tensor_image


NODE_CLASS_MAPPINGS.update(comfy_annotations.NODE_CLASS_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS.update(comfy_annotations.NODE_DISPLAY_NAME_MAPPINGS)

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
