from typing_extensions import Tuple
from config import ENV_VARIABLES_EXPECTED
from services.LoggerService import LoggerService

from dotenv import load_dotenv, dotenv_values
from services.TelegramService import TelegramService
load_dotenv()

class App:
    """
    # App class
    """

    def __init__(self) -> None:
        self.__logger__ = LoggerService()
        self.__config__ = dotenv_values(".env")
        pass

    def set_service(self, service: TelegramService) -> None:
        self.__telegram_service__ = service

        api_key = self.__config__.get("API_KEY")
        self.__telegram_service__.set_api_key(api_key=api_key)

    def run(self):
        try:
            self.__telegram_service__.run()
        except Exception as e:
            error_string = str(e)
            self.__logger__.error(error_string)

    def verify_env_variables(self) -> Tuple[bool, str]:
        for var in ENV_VARIABLES_EXPECTED:
            if not self.__config__.get(var):
                error = self.__logger__.error(fr'{var} not found.')
                return (False, error)

        success = self.__logger__.info("ENV variables successfully loaded!")
        return (True, success)
