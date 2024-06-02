from fastapi import FastAPI, Request, Response, status

from services.browser_settings.errors import (
    BrowserSettingsAlreadyExistsError,
    BrowserSettingsNotFoundError,
)


async def browser_context_already_exists_handler(
    _: Request, exc: BrowserSettingsAlreadyExistsError
) -> Response:
    return Response(
        content=b"",
        status_code=status.HTTP_409_CONFLICT,
        headers={
            "X-Context-Name": exc.name,
        },
    )


async def browser_context_not_found_handler(
    _: Request, exc: BrowserSettingsNotFoundError
) -> Response:
    return Response(
        content=b"",
        status_code=status.HTTP_404_NOT_FOUND,
        headers={
            "X-Context-Name": exc.name,
        },
    )


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        BrowserSettingsAlreadyExistsError, browser_context_already_exists_handler
    )
    app.add_exception_handler(
        BrowserSettingsNotFoundError, browser_context_not_found_handler
    )
