import dataclasses
import docspec
import typing as t
from pathlib import Path
from pydoc_markdown.interfaces import Context, Renderer
from pydoc_markdown.contrib.renderers.markdown import MarkdownRenderer


def get_first_class(modules: t.List[docspec.Module]) -> t.Optional[docspec.Class]:
    if not modules:
        return None

    for i in modules:
        if isinstance(i, docspec.Class):
            return i

        child = get_first_class(getattr(i, "members", []))
        if child:
            return child


def sanitize(s: str) -> str:
    character_map = {
        r"_": r"\_",
        r"<": r"\<",
        r">": r"\>",
    }

    for before, after in character_map.items():
        s = s.replace(before, after)
    return s


@dataclasses.dataclass
class RucioRenderer(Renderer):

    markdown: MarkdownRenderer = dataclasses.field(default_factory=MarkdownRenderer)

    def init(self, context: Context) -> None:
        self.markdown.init(context)

    def render_recursive(self, obj: docspec.ApiObject) -> None:
        if isinstance(obj, docspec.Function):
            # print(f"<div style=\"visibility: hidden\">\n## {sanitize(obj.name)}\n</div>\n")
            print(f"## {sanitize(obj.name)}\n")
            if obj.docstring:
                print(obj.docstring.content + "\n")

        for item in getattr(obj, "members", []):
            self.render_recursive(item)

    def render(self, modules: t.List[docspec.Module]) -> None:
        print("---")
        print(f"title: {get_first_class(modules).name}")
        print("---")

        
        for module in modules:
            self.render_recursive(module)