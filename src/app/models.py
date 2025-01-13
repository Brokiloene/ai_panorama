from pydantic import BaseModel

class Article(BaseModel):
    image_path: str|None
    title: str
    article_text: str
