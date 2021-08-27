import dataclasses


@dataclasses.dataclass
class Error:
    error_msg: str

    def __post_init__(self):
        self.error_msg = f"{type(self).__name__}: {self.error_msg}"


class GlobalError(Error):
    """A global error in BiBTeX file"""


class EntryError(Error):
    """An error with a BiBTeX Entry"""


class FieldError(Error):
    """An error with a BiBTeX Field"""
