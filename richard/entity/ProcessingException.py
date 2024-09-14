from dataclasses import dataclass


@dataclass
class ProcessingException(BaseException):
    error: str
