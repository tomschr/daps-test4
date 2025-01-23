"""
Our custom exception classes
"""

class NoConfigFilesFoundError(FileNotFoundError):
    pass


# --- Configuration exceptions
class BaseConfigError(ValueError):
    def __init__(self, error, *args, **kwargs):
        self.error = error
        super().__init__(*args, **kwargs)


class MissingSectionError(BaseConfigError):
    """A missing section could not be found in the config"""

    def __str__(self) -> str:
        return f"Missing section in config file: {self.error}"


class MissingKeyError(BaseConfigError):
    """A missing key could not be found in the config"""

    def __str__(self) -> str:
        return f"Missing key in config file: {self.error}"


# --- Validator exceptions, base classes
class BaseMetadataError(ValueError):
    """Base class for metadata errors"""
    pass


class BaseMetadataWarning(ValueError):
    """Base class for metadata warnings"""
    pass


# --- Warnings
class MissingAttributeWarning(BaseMetadataWarning):
    """A warning for a missing attribute that is recommended to have"""
    def __str__(self) -> str:
        return f"Missing recommended attribute in {super().__str__()}"


# --- Errors
# class InvalidElementError(BaseMetadataError):
#     """An element was missing or invalid in the metadata"""
#     def __str__(self) -> str:
#         return f"Missing or invalid element in {super().__str__()}"


class InvalidValueError(BaseMetadataError):
    """A value was invalid in the metadata"""
    def __str__(self) -> str:
        return f"Invalid value in metadata {super().__str__()}"
