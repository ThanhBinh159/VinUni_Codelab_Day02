import importlib.util
from pathlib import Path

from PIL import Image


RENDERER_PATH = (
    Path(__file__).parents[1] / "tools" / "render_workflow_diagram.py"
)


def test_render_creates_readable_1600_by_900_png(tmp_path):
    assert RENDERER_PATH.exists(), "workflow renderer is missing"
    spec = importlib.util.spec_from_file_location("workflow_renderer", RENDERER_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    output = module.render(tmp_path / "workflow.png")

    with Image.open(output) as image:
        assert image.format == "PNG"
        assert image.size == (1600, 900)
        assert image.mode == "RGB"
        colors = image.getcolors(maxcolors=1_000_000)
        assert colors is not None and len(colors) >= 8
