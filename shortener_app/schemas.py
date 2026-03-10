from pydantic import BaseModel


class URLBase(BaseModel):
    target_url: str
    custom_url: str | None = None


class URL(URLBase):
    is_active: bool
    clicks: int

    model_config = ConfigDict(from_attributes=True)


class URLInfo(URL):
    url: str
    admin_url: str
