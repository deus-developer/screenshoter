from typing import Optional, Literal, List

from pydantic import BaseModel, UUID4, ConfigDict, Field


class ClipSettings(BaseModel):
    x: float
    y: float
    width: float
    height: float


class ViewportSettings(BaseModel):
    width: int
    height: int


class GeoLocationSettings(BaseModel):
    latitude: float
    longitude: float
    accuracy: Optional[float] = None


class BrowserSettings(BaseModel):
    name: UUID4 = Field(description="ID контекста")

    viewport: Optional[ViewportSettings] = Field(None, description="Настройки экрана")
    geolocation: Optional[GeoLocationSettings] = Field(
        None, description="Настройки геологации"
    )

    ignore_https_errors: bool = Field(True, description="Игнорирование ошибок SSL")
    java_script_enabled: bool = Field(True, description="javascript enabled")

    user_agent: Optional[str] = Field(None, description="user-agent")
    locale: Optional[str] = Field("ru-RU", description="Locale")
    timezone: Optional[str] = Field("Europe/Moscow", description="Timezone")

    device_scale_factor: float = 1.0
    is_mobile: bool = Field(False, description="Мобильное устройство")
    has_touch: bool = Field(False, description="Имеется ли touch screen")
    color_scheme: Literal["dark", "light", "no-preference", "null"] = Field(
        "light", description="Цветовая схема браузера"
    )
    accept_downloads: bool = Field(
        True, description="Разрешить автоматическую загрузку файлов"
    )
    service_workers: Literal["allow", "block"] = "allow"
    bypass_csp: bool = True
    permissions: Optional[
        List[
            Literal[
                "geolocation",
                "notifications",
                "background-sync",
                "clipboard-read",
                "clipboard-write",
            ]
        ]
    ] = None

    model_config = ConfigDict(extra="ignore")
