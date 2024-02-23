import speech_recognition as sr
from services.AudioService import AudioService

class TranscribeService:
    """
    # Transcribe Service class
    """

    def __init__(self) -> None:
        self.__audio_service__ = AudioService()
        pass

    def transcribe(self, array: bytearray) -> str:
        audio_buffer = self.__audio_service__.convert_bytearray_to_audio_buffer(array=array)

        recognizer_instance = sr.Recognizer()
        with sr.AudioFile(audio_buffer) as source:
            audio_data  = recognizer_instance.record(source=source)
            json_string = recognizer_instance.recognize_vosk(audio_data=audio_data)

            return json_string

        return ""
