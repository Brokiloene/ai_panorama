from enum import Enum, unique

from app import config
from app.exceptions import ViewTemplateNotFoundError
from app.models import Article


@unique
class HTMLTemplate(Enum):
    INDEX = "index.jinja"
    LOAD_ARTICLES = "form_news.jinja"


def html_render(template_name: HTMLTemplate, data: list[Article]):
    """
    Рендерит HTML страницу новостей по данному списку Article
    и названию шаблона

    :raises: `ViewTemplateNotFoundError`
    """
    template = config.html.html_render_env.get_template(name=template_name.value)
    match template_name:
        case HTMLTemplate.INDEX:
            prerendered_data = html_render(HTMLTemplate.LOAD_ARTICLES, data)
            return template.render(data=prerendered_data)
        case HTMLTemplate.LOAD_ARTICLES:
            return template.render(articles_list=data)
    raise ViewTemplateNotFoundError(f"Could not find template {template_name}")
