from typing import Dict, Any
from jinja2 import Environment, FileSystemLoader, Template


class PromptManager:
    def __init__(self, template_dir: str = "prompts") -> None:
        self.env = Environment(loader=FileSystemLoader(template_dir))

    def render(self, template_name: str, context: Dict[str, Any]) -> str:
        template: Template = self.env.get_template(template_name)
        return template.render(**context)
