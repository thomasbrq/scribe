from json.decoder import JSONDecoder
from typing import Callable
from types import FunctionType
from typing_extensions import Any, Coroutine, Dict, List
from warnings import filters
from services.LoggerService import LoggerService
from services.TranscribeService import TranscribeService
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from telegram.constants import ParseMode
from dataclasses import dataclass
import json

@dataclass
class Command:
    name: str
    fn: Callable[[Update, ContextTypes], Coroutine]

@dataclass
class Context:
    update: Update
    context: ContextTypes

class TelegramService:
    """
    # TelegramService class
    """

    def set_api_key(self, api_key: str) -> None:
        self.__api_key__ = api_key

    def run(self) -> None:
        self.__app__ = ApplicationBuilder().token(self.__api_key__).build()
        self.__logger__.info("Bot is running.")

        commands = [
            Command(name="ping", fn=self.__ping__),
            Command(name="start", fn=self.__start__),
        ]
        self.__add_commands__(commands=commands)

        attachment_handler = MessageHandler(filters=filters.ATTACHMENT, callback=self.__handle_attachments__)
        self.__app__.add_handler(attachment_handler)

        self.__app__.run_polling()

    def __init__(self) -> None:
        self.__logger__ = LoggerService()
        self.__transcribe_service = TranscribeService()
        pass

    def __add_commands__(self, commands: List[Command]) -> None:
        for command in commands:
            self.__app__.add_handler( CommandHandler(command.name, command.fn) )
            self.__logger__.info(fr"'{command.name}' command successfully added.")

    async def __reply_to_user__(self, ctx: Context, message: str, markdown=False) -> None:
        if markdown == True:
            await ctx.context.bot.send_message(chat_id=ctx.update.effective_chat.id, text=message, parse_mode=ParseMode.MARKDOWN_V2)
        else:
            await ctx.context.bot.send_message(chat_id=ctx.update.effective_chat.id, text=message)

    async def __reply_to_user_with_error__(self, ctx: Context, message: str) -> None:
        await ctx.context.bot.send_message(chat_id=ctx.update.effective_chat.id, text=fr"❌{message}")

    async def __start__(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        first_name = update.message.chat.first_name
        message = fr"Hello {first_name}, send me an audio and I will transcribe it for you!"

        ctx = Context(update=update, context=context)
        await self.__reply_to_user__(ctx=ctx, message=message)

    async def __ping__(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        ctx = Context(update=update, context=context)
        await self.__reply_to_user__(ctx=ctx, message="pong!")

    async def __handle_attachments__(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        self.__logger__.info("attachment received")

        audio = update.message.audio
        if not audio:
            error_string = self.__logger__.error("The file received is not an audio")
            ctx = Context(update=update, context=context)
            await self.__reply_to_user_with_error__(ctx=ctx, message=error_string)
            return

        try:
            attachment                  = await audio.get_file()
            attachment_bytes_array      = await attachment.download_as_bytearray()

            json_string                 = self.__transcribe_service.transcribe(attachment_bytes_array)
            decoded_json                = json.loads(json_string)

            ctx = Context(update=update, context=context)

            message = decoded_json["text"]
            await self.__reply_to_user__(ctx=ctx, message=fr">{message}", markdown=True)
        except Exception as e:
            error_string = str(e)
            self.__logger__.error(error_string)
            ctx = Context(update=update, context=context)
            await self.__reply_to_user_with_error__(ctx=ctx, message="Unable to transcribe your audio. The format may not be supported, or your file may be corrupted.")
