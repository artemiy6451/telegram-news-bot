"""File for import tamplates to project."""

import jinja2

from telegram_news_bot.config import settings

template_loader = jinja2.FileSystemLoader(
    searchpath=settings.base_dir / settings.template_dir
)
env = jinja2.Environment(
    loader=template_loader,
    trim_blocks=True,
    lstrip_blocks=True,
)


def render_template(template_name: str, data: dict | None = None) -> str:
    """Render jinja2 template."""
    if data is None:
        data = {}
    template = env.get_template(template_name)
    rendered = template.render(**data)
    rendered = rendered.replace("'", '"')
    return rendered
