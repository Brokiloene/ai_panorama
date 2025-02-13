import app.config as config
from app.models import Article


def html_view(template_name: str, data: list[Article]):
    template = config.html.html_render_env.get_template(name=template_name)
    if template_name == "index.jinja":
        prerendered_data = html_view("form_news.jinja", data)
        return template.render(data=prerendered_data)
    elif template_name == "form_news.jinja":
        return template.render(news_list=data)
