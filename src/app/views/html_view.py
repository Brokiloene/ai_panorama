from app import config
from app.exceptions import ViewTemplateNotFoundError
from app.models import Article


def html_render(template_name: str, data: list[Article]):
    """
    Рендерит HTML страницу новостей по данному списку Article
    и названию шаблона

    :raises: `ViewTemplateNotFoundError`
    """
    template = config.html.html_render_env.get_template(name=template_name)
    if template_name == "index.jinja":
        prerendered_data = html_render("form_news.jinja", data)
        return template.render(data=prerendered_data)
    if template_name == "form_news.jinja":
        return template.render(news_list=data)
    raise ViewTemplateNotFoundError(f"Could not find template {template_name}")
