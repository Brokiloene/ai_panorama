import jinja2

from . import app

html_render_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(searchpath=app.TEMPLATES_DIR),
    autoescape=jinja2.select_autoescape(),
)

NEWS_LOAD_BATCH_SIZE = 9
