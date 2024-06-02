from typing import Optional, Literal

from pydantic import BaseModel, Field, HttpUrl

from services.browser.schemas import ClipSettings


class ScreenshotRequest(BaseModel):
    url: HttpUrl = Field(description="Ссылка на сайт")
    referer: Optional[HttpUrl] = Field(None, description="Источник перехода")
    omit_background: bool = Field(False, description="")
    full_page: bool = Field(False, description="Скриншот всей страницы")
    clip_settings: Optional[ClipSettings] = Field(None, description="Рамка скриншота")
    animations: Literal["allow", "disabled"] = Field("allow", description="Анимации")

    timeout: float = Field(
        60.0, description="Ожидание открытия страницы", gt=0, le=300.0
    )
    wait: float = Field(0.0, description="Ожидание перед скриншотом", gt=0, le=300.0)
