from pydantic import UUID4


class BrowserSettingsServiceError(Exception):
    pass


class BrowserSettingsAlreadyExistsError(BrowserSettingsServiceError):
    def __init__(self, name: UUID4):
        self.name = str(name)


class BrowserSettingsNotFoundError(BrowserSettingsServiceError):
    def __init__(self, name: UUID4):
        self.name = str(name)
