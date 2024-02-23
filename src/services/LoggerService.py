import sys

class LoggerService:
    """
    # LoggerService class
    """

    def __init__(self) -> None:
        pass

    def __format_log__(self, level: str, message: str) -> str:
        return "{level}: {message}".format(level=level, message=message)

    def error(self, message: str) -> str:
        formatted_log = self.__format_log__(level="ERROR", message=message)
        print(formatted_log, file=sys.stderr)
        return message

    def info(self, message: str) -> str:
        formatted_log = self.__format_log__(level="INFO", message=message)
        print(formatted_log, file=sys.stdout)
        return message
