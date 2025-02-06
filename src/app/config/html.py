import jinja2

from . import system

html_render_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(searchpath=system.TEMPLATES_DIR), 
    autoescape=jinja2.select_autoescape()
)

NEWS_LOAD_BATCH_SIZE = 9
