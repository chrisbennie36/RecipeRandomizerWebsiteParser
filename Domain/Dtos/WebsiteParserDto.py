from pydantic import BaseModel

class WebsiteParserDto(BaseModel):
    url: str